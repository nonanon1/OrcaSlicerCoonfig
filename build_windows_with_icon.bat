@echo off
echo Building OrcaSlicer Configuration Manager for Windows with skull icon...
echo.

:: Check if icon exists
if not exist "skull_icon.ico" (
    echo WARNING: skull_icon.ico not found. Building without icon.
    echo To add skull icon: Place skull_icon.ico file in this directory and run again.
    echo.
    set ICON_PARAM=
) else (
    echo Using skull_icon.ico
    set ICON_PARAM=--icon=skull_icon.ico
)

:: Install PyInstaller if not already installed
pip install pyinstaller

:: Build the executable with icon
pyinstaller --onefile --windowed --name "OrcaSlicer-Config-Manager" %ICON_PARAM% main.py

echo.
echo Build complete! Executable is in the 'dist' folder.
echo File: dist\OrcaSlicer-Config-Manager.exe
echo.
pause