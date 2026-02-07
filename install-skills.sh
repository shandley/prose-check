#!/bin/bash
#
# prose-check skill installer
# Installs writing skills for Claude Code
#
# Usage:
#   ./install-skills.sh              # Install to current project
#   ./install-skills.sh --global     # Install to ~/.claude/skills/
#   ./install-skills.sh --help       # Show help
#
# Or via curl:
#   curl -fsSL https://raw.githubusercontent.com/shandley/prose-check/main/install-skills.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/shandley/prose-check/main/install-skills.sh | bash -s -- --global

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Skills to install
SKILLS=(
    "human-writing"
    "manuscript-writing"
    "revision-workflow"
    "submission-prep"
    "scientific-style"
    "scientific-figures"
    "bibliography"
)

REPO_URL="https://github.com/shandley/prose-check"
RAW_URL="https://raw.githubusercontent.com/shandley/prose-check/main"

usage() {
    echo "prose-check skill installer"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --global, -g    Install to ~/.claude/skills/ (available in all projects)"
    echo "  --local, -l     Install to ./.claude/skills/ (current project only, default)"
    echo "  --list          List available skills without installing"
    echo "  --help, -h      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Install to current project"
    echo "  $0 --global           # Install globally"
    echo "  $0 --list             # Show available skills"
    echo ""
    echo "Skills included:"
    echo "  human-writing         Natural prose style, avoids AI patterns"
    echo "  manuscript-writing    IMRaD structure, abstracts, academic papers"
    echo "  revision-workflow     Peer review responses, change tracking"
    echo "  submission-prep       Cover letters, checklists, figures/tables"
    echo "  scientific-style      Citations, hedging, claim calibration"
    echo "  scientific-figures    AI figure generation, review, and revision"
    echo "  bibliography          Audit, fix, and format bibliographies"
}

list_skills() {
    echo -e "${BLUE}Available prose-check skills:${NC}"
    echo ""
    echo -e "  ${GREEN}human-writing${NC}"
    echo "    Write in natural, human style. Avoids AI writing patterns."
    echo "    Use for: essays, papers, documentation, articles"
    echo ""
    echo -e "  ${GREEN}manuscript-writing${NC}"
    echo "    Structure academic papers using IMRaD format."
    echo "    Use for: research papers, abstracts, section organization"
    echo ""
    echo -e "  ${GREEN}revision-workflow${NC}"
    echo "    Respond to peer review and manage revisions."
    echo "    Use for: response letters, tracking changes, reviewer concerns"
    echo ""
    echo -e "  ${GREEN}submission-prep${NC}"
    echo "    Prepare manuscripts for journal submission."
    echo "    Use for: cover letters, checklists, figure/table specs"
    echo ""
    echo -e "  ${GREEN}scientific-style${NC}"
    echo "    Calibrate claims and integrate citations."
    echo "    Use for: hedging language, citation patterns, claim strength"
    echo ""
    echo -e "  ${GREEN}scientific-figures${NC}"
    echo "    Generate and review scientific figures with AI."
    echo "    Use for: figure generation, visual review, manuscript alignment"
    echo ""
    echo -e "  ${GREEN}bibliography${NC}"
    echo "    Audit, fix, and format bibliographies."
    echo "    Use for: citation cross-referencing, orphan detection, reference formatting"
    echo ""
}

# Parse arguments
INSTALL_DIR=""
GLOBAL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --global|-g)
            GLOBAL=true
            shift
            ;;
        --local|-l)
            GLOBAL=false
            shift
            ;;
        --list)
            list_skills
            exit 0
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            exit 1
            ;;
    esac
done

# Set install directory
if [ "$GLOBAL" = true ]; then
    INSTALL_DIR="$HOME/.claude/skills"
    echo -e "${BLUE}Installing skills globally to ${INSTALL_DIR}${NC}"
else
    INSTALL_DIR=".claude/skills"
    echo -e "${BLUE}Installing skills to ${INSTALL_DIR} (current project)${NC}"
fi

# Create directory
mkdir -p "$INSTALL_DIR"

# Check if we're in the prose-check repo (local install)
if [ -d ".claude/skills/human-writing" ] && [ -f "install-skills.sh" ]; then
    echo -e "${YELLOW}Detected local prose-check repository${NC}"
    SOURCE_DIR=".claude/skills"

    for skill in "${SKILLS[@]}"; do
        if [ -d "$SOURCE_DIR/$skill" ]; then
            if [ "$GLOBAL" = true ] || [ "$SOURCE_DIR" != "$INSTALL_DIR" ]; then
                echo -e "  Installing ${GREEN}$skill${NC}..."
                cp -r "$SOURCE_DIR/$skill" "$INSTALL_DIR/"
            else
                echo -e "  ${YELLOW}$skill${NC} already in place"
            fi
        fi
    done
else
    # Download from GitHub
    echo -e "${BLUE}Downloading skills from GitHub...${NC}"

    # Check for curl or wget
    if command -v curl &> /dev/null; then
        FETCH="curl -fsSL"
    elif command -v wget &> /dev/null; then
        FETCH="wget -qO-"
    else
        echo -e "${RED}Error: curl or wget required${NC}"
        exit 1
    fi

    # Create temp directory
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR" EXIT

    # Clone just the skills directory (sparse checkout)
    echo -e "  Fetching skill files..."

    cd "$TEMP_DIR"
    git clone --depth 1 --filter=blob:none --sparse "$REPO_URL.git" prose-check 2>/dev/null || {
        echo -e "${RED}Error: Failed to clone repository${NC}"
        echo "Make sure git is installed and you have internet access"
        exit 1
    }

    cd prose-check
    git sparse-checkout set .claude/skills 2>/dev/null

    # Copy skills to install directory
    cd - > /dev/null
    for skill in "${SKILLS[@]}"; do
        if [ -d "$TEMP_DIR/prose-check/.claude/skills/$skill" ]; then
            echo -e "  Installing ${GREEN}$skill${NC}..."
            cp -r "$TEMP_DIR/prose-check/.claude/skills/$skill" "$INSTALL_DIR/"
        else
            echo -e "  ${YELLOW}Warning: $skill not found${NC}"
        fi
    done
fi

# Verify installation
echo ""
echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "Installed skills:"
for skill in "${SKILLS[@]}"; do
    if [ -d "$INSTALL_DIR/$skill" ]; then
        echo -e "  ${GREEN}✓${NC} $skill"
    else
        echo -e "  ${RED}✗${NC} $skill (not found)"
    fi
done

echo ""
echo -e "${BLUE}Usage:${NC}"
echo "  Skills activate automatically based on context, or invoke directly:"
echo "    /human-writing [topic]"
echo "    /manuscript-writing [section]"
echo "    /revision-workflow [reviewer comment]"
echo "    /submission-prep [task]"
echo "    /scientific-style [text to review]"
echo "    /scientific-figures [figure description]"
echo "    /bibliography [audit manuscript.md]"
echo ""

# Make scripts executable
for skill in "${SKILLS[@]}"; do
    if [ -d "$INSTALL_DIR/$skill/scripts" ]; then
        chmod +x "$INSTALL_DIR/$skill/scripts/"*.py 2>/dev/null || true
    fi
done

if [ "$GLOBAL" = true ]; then
    echo -e "${YELLOW}Note:${NC} Global skills are available in all Claude Code projects."
else
    echo -e "${YELLOW}Note:${NC} Skills installed to current project only."
    echo "      Use --global to install for all projects."
fi
