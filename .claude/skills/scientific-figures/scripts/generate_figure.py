#!/usr/bin/env python3
"""
Scientific Figure Generator
Generates and edits scientific figures using Google's Gemini image models.

Extends the base gemini-image generator with:
- Multi-turn editing (--input-image for iterative revision)
- Scientific style presets (--style scientific)
- Size control (--size 1k/2k/4k)
- JSON metadata output to stderr
- Automatic retry on transient failures
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# Scientific style preamble prepended when --style scientific is used
SCIENTIFIC_PREAMBLE = (
    "Create a clean, publication-quality scientific figure. "
    "Use a white background, high contrast, and sans-serif font labels "
    "(Arial or Helvetica). No watermarks, no decorative elements. "
    "Ensure all text is legible at print size (minimum 8pt equivalent). "
    "Use a colorblind-safe color palette (e.g., Wong palette or viridis). "
)

SIZE_PRESETS = {
    "1k": "Generate at approximately 1024x1024 pixels.",
    "2k": "Generate at approximately 2048x2048 pixels for high resolution.",
    "4k": "Generate at approximately 4096x4096 pixels for maximum print quality.",
}

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def load_api_key():
    """Load API key from environment or .env file."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        return api_key

    search_paths = [
        Path.cwd() / ".env",
        Path.cwd().parent / ".env",
        Path.cwd().parent.parent / ".env",
        Path.home() / ".env",
    ]

    for env_path in search_paths:
        if env_path.exists():
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GOOGLE_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")

    raise ValueError(
        "GOOGLE_API_KEY not found. Set it as an environment variable "
        "or add it to a .env file in your project directory."
    )


def build_prompt(base_prompt, style=None, size=None):
    """Build the full prompt with optional style and size modifiers."""
    parts = []

    if style == "scientific":
        parts.append(SCIENTIFIC_PREAMBLE)

    parts.append(base_prompt)

    if size and size in SIZE_PRESETS:
        parts.append(SIZE_PRESETS[size])

    return " ".join(parts)


def load_image_bytes(image_path):
    """Load an image file and return bytes and MIME type."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Input image not found: {image_path}")

    suffix = path.suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    mime_type = mime_map.get(suffix, "image/png")

    with open(path, "rb") as f:
        return f.read(), mime_type


def detect_image_format(data):
    """Detect image format from file header bytes."""
    if data[:3] == b"\xff\xd8\xff":
        return "jpeg"
    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    elif data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    elif data[:3] == b"GIF":
        return "gif"
    return "unknown"


def correct_extension(output_path, detected_format):
    """Correct file extension to match actual image format.

    Gemini typically returns JPEG data regardless of requested extension.
    This ensures the saved file has the correct extension.
    """
    ext_map = {
        "jpeg": ".jpg",
        "png": ".png",
        "webp": ".webp",
        "gif": ".gif",
    }
    if detected_format not in ext_map:
        return output_path

    expected_ext = ext_map[detected_format]
    current_ext = output_path.suffix.lower()

    # .jpg and .jpeg are equivalent
    if detected_format == "jpeg" and current_ext in (".jpg", ".jpeg"):
        return output_path
    if current_ext == expected_ext:
        return output_path

    corrected = output_path.with_suffix(expected_ext)
    print(
        f"Note: Gemini returned {detected_format.upper()} data. "
        f"Saving as {corrected.name} instead of {output_path.name}",
        file=sys.stderr,
    )
    return corrected


def emit_metadata(metadata):
    """Write JSON metadata to stderr for structured output."""
    print(json.dumps(metadata), file=sys.stderr)


def generate_figure(prompt, output_path=None, input_image=None, style=None, size=None):
    """
    Generate or edit a scientific figure using Gemini.

    Args:
        prompt: Text description or edit instructions
        output_path: Where to save the generated image
        input_image: Path to existing image for multi-turn editing
        style: Style preset ("scientific" or None)
        size: Size preset ("1k", "2k", "4k", or None)

    Returns:
        dict with success status, path, and metadata
    """
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("Installing google-genai...", file=sys.stderr)
        os.system(f"{sys.executable} -m pip install google-genai pillow")
        from google import genai
        from google.genai import types

    api_key = load_api_key()

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"figure_{timestamp}.png"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    full_prompt = build_prompt(prompt, style=style, size=size)
    mode = "edit" if input_image else "generate"

    print(f"Mode: {mode}", file=sys.stderr)
    print(f"Prompt: {full_prompt[:150]}...", file=sys.stderr)

    # Build content parts
    contents = []
    if input_image:
        image_bytes, mime_type = load_image_bytes(input_image)
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
        contents.append(f"Edit this image: {full_prompt}")
    else:
        contents.append(f"Generate an image: {full_prompt}")

    client = genai.Client(api_key=api_key)

    models_to_try = [
        "gemini-3-pro-image-preview",
        "gemini-2.0-flash-exp",
    ]

    last_error = None

    for model_name in models_to_try:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(
                    f"Trying {model_name} (attempt {attempt}/{MAX_RETRIES})...",
                    file=sys.stderr,
                )

                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE", "TEXT"],
                    ),
                )

                # Extract image from response parts
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        image_data = part.inline_data.data
                        detected_fmt = detect_image_format(image_data)
                        actual_path = correct_extension(output_path, detected_fmt)
                        with open(actual_path, "wb") as f:
                            f.write(image_data)

                        metadata = {
                            "success": True,
                            "path": str(actual_path),
                            "detected_format": detected_fmt,
                            "model": model_name,
                            "mode": mode,
                            "style": style,
                            "size": size,
                            "prompt": full_prompt,
                            "input_image": str(input_image) if input_image else None,
                            "attempt": attempt,
                            "timestamp": datetime.now().isoformat(),
                        }
                        print(f"Image saved to: {actual_path}")
                        emit_metadata(metadata)
                        return metadata

                # Check for generated_images attribute (older API format)
                if hasattr(response, "generated_images") and response.generated_images:
                    image = response.generated_images[0]
                    image.image.save(str(output_path))

                    metadata = {
                        "success": True,
                        "path": str(output_path),
                        "model": model_name,
                        "mode": mode,
                        "style": style,
                        "size": size,
                        "prompt": full_prompt,
                        "input_image": str(input_image) if input_image else None,
                        "attempt": attempt,
                        "timestamp": datetime.now().isoformat(),
                    }
                    print(f"Image saved to: {output_path}")
                    emit_metadata(metadata)
                    return metadata

                last_error = "No image in response"
                print(f"No image in response from {model_name}", file=sys.stderr)
                break  # No point retrying if no image returned

            except Exception as e:
                last_error = str(e)
                print(f"Error: {last_error}", file=sys.stderr)
                if attempt < MAX_RETRIES:
                    print(f"Retrying in {RETRY_DELAY}s...", file=sys.stderr)
                    time.sleep(RETRY_DELAY)

    # All models and retries exhausted
    metadata = {
        "success": False,
        "error": last_error,
        "mode": mode,
        "style": style,
        "prompt": full_prompt,
    }
    print(f"Generation failed: {last_error}")
    emit_metadata(metadata)
    return metadata


def main():
    parser = argparse.ArgumentParser(
        description="Generate scientific figures using Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic scientific figure
  %(prog)s "workflow diagram showing DNA extraction to sequencing" --style scientific

  # Edit an existing figure
  %(prog)s "make the labels larger and add a scale bar" --input-image fig1.png

  # High-resolution output
  %(prog)s "bar chart of gene expression" --style scientific --size 2k --output figures/fig2.png

  # Validate API key
  %(prog)s --validate
""",
    )
    parser.add_argument(
        "prompt",
        type=str,
        nargs="?",
        default=None,
        help="Text description of the figure to generate, or edit instructions",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output path for the generated image (default: figure_TIMESTAMP.png)",
    )
    parser.add_argument(
        "--input-image",
        "-i",
        type=str,
        default=None,
        help="Path to existing image for multi-turn editing",
    )
    parser.add_argument(
        "--style",
        "-s",
        type=str,
        choices=["scientific"],
        default=None,
        help="Style preset to apply (scientific adds clean pub-quality instructions)",
    )
    parser.add_argument(
        "--size",
        type=str,
        choices=["1k", "2k", "4k"],
        default=None,
        help="Target output size (1k=1024px, 2k=2048px, 4k=4096px)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate API key configuration and exit",
    )

    args = parser.parse_args()

    if args.validate:
        try:
            api_key = load_api_key()
            print(f"API key found: {api_key[:10]}...{api_key[-4:]}")
            print("Configuration is valid!")
            return
        except Exception as e:
            print(f"Configuration error: {e}")
            sys.exit(1)

    if not args.prompt:
        parser.error("prompt is required when not using --validate")

    result = generate_figure(
        prompt=args.prompt,
        output_path=args.output,
        input_image=args.input_image,
        style=args.style,
        size=args.size,
    )

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
