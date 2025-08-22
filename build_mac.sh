#!/bin/bash
echo "Building OrcaSlicer Configuration Manager for Mac..."
echo

# Install PyInstaller if not already installed
pip3 install pyinstaller

# Build the executable
pyinstaller --onefile --windowed --name "OrcaSlicer-Config-Manager" main.py

echo
echo "Build complete! Executable is in the 'dist' folder."
echo "To create a .app bundle, the executable is ready to use."