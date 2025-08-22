@echo off
echo Building OrcaSlicer Configuration Manager for Windows...
echo.

:: Install PyInstaller if not already installed
pip install pyinstaller

:: Build the executable
pyinstaller --onefile --windowed --name "OrcaSlicer-Config-Manager" --icon=icon.ico main.py

echo.
echo Build complete! Executable is in the 'dist' folder.
echo.
pause