#!/bin/bash
# Mac launcher for AncesTree
# This file can be double-clicked to start AncesTree

# Change to project root (parent of scripts directory)
cd "$(dirname "$0")/.."

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    python3 scripts/launcher.py
else
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org"
    read -p "Press Enter to exit..."
fi
