@echo off
echo Building OrcaSlicer Configuration Manager for Windows...
echo.

:: Install PyInstaller if not already installed
python -m pip install pyinstaller

:: Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

:: Build the executable
pyinstaller --onefile --windowed --name "OrcaSlicer-Config-Manager" main.py

echo.
echo ✅ Build complete!
echo 📦 Windows executable created: dist\OrcaSlicer-Config-Manager.exe
echo 🚀 You can now distribute the executable file
echo.
echo To test the executable:
echo   dist\OrcaSlicer-Config-Manager.exe
echo.
pause