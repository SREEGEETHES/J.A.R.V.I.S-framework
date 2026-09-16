#!/usr/bin/env bash
# JARVIS-FRAMEWORK Universal Installer
set -e

if [ "$1" == "--global" ] || [ "$1" == "-g" ]; then
    echo "Installing JARVIS globally for Antigravity, OpenCode, and Claude Code..."
    mkdir -p "$HOME/.gemini/config/skills"
    mkdir -p "$HOME/.config/opencode/commands"
    mkdir -p "$HOME/.claude/commands"

    cp -r .agents/skills/* "$HOME/.gemini/config/skills/" 2>/dev/null || true
    cp -r .opencode/commands/* "$HOME/.config/opencode/commands/" 2>/dev/null || true
    cp -r .claude/commands/* "$HOME/.claude/commands/" 2>/dev/null || true

    echo "JARVIS-FRAMEWORK installed globally! Available across all your projects."
    exit 0
fi

TARGET_DIR="${1:-.}"
echo "Installing JARVIS-FRAMEWORK into: $TARGET_DIR..."

mkdir -p "$TARGET_DIR"
cp -r .jarvis "$TARGET_DIR/"
cp -r .agents "$TARGET_DIR/"
mkdir -p "$TARGET_DIR/.opencode/commands"
cp .opencode/AGENTS.md "$TARGET_DIR/.opencode/" 2>/dev/null || true
cp .opencode/commands/* "$TARGET_DIR/.opencode/commands/" 2>/dev/null || true
cp -r .claude "$TARGET_DIR/"
cp .clinerules "$TARGET_DIR/" 2>/dev/null || true
cp .cursorrules "$TARGET_DIR/" 2>/dev/null || true
cp CLAUDE.md "$TARGET_DIR/" 2>/dev/null || true
cp GEMINI.md "$TARGET_DIR/" 2>/dev/null || true
cp .windsurfrules "$TARGET_DIR/" 2>/dev/null || true

echo "JARVIS-FRAMEWORK successfully installed in $TARGET_DIR for all IDEs!"
