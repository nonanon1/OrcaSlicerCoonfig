# OrcaSlicer Configuration Manager

A GUI application for backing up, restoring, and comparing OrcaSlicer configurations across different platforms.

## Building the Application

This application can be built for both macOS and Windows as standalone executables that don't require Python to be installed.

### 🍎 Building for macOS

**Requirements:**
- macOS 10.15 or later
- Python 3.7+ installed
- Run on the target Mac system (Intel or Apple Silicon)

**Build Steps:**

1. **Download/Clone the project files to your Mac**

2. **Open Terminal and navigate to the project folder:**
   ```bash
   cd path/to/OrcaSlicer-Config-Manager
   ```

3. **Make the build script executable and run it:**
   ```bash
   chmod +x build_mac.sh
   ./build_mac.sh
   ```

**Alternative Manual Build:**
```bash
# Install PyInstaller
python3 -m pip install pyinstaller

# Clean previous builds
rm -rf build dist *.spec

# Build the executable
pyinstaller --onefile --windowed --name "OrcaSlicer-Config-Manager" main.py

# The script will create the complete .app bundle automatically
```

**Result:**
- Complete `.app` bundle: `dist/OrcaSlicer Configuration Manager.app`
- Ready to drag to Applications folder or distribute
- Works on macOS 10.15+ (Intel and Apple Silicon compatible)

---

### 🪟 Building for Windows

**Requirements:**
- Windows 10 or later
- Python 3.7+ installed
- Must be run on a Windows system

**Build Steps:**

1. **Download/Extract the project files to your Windows machine**

2. **Open Command Prompt or PowerShell and navigate to the project folder:**
   ```cmd
   cd C:\path\to\OrcaSlicer-Config-Manager
   ```

3. **Run the build script:**
   ```cmd
   build_windows.bat
   ```

**Alternative Manual Build:**
```cmd
# Install PyInstaller
python -m pip install pyinstaller

# Clean previous builds
rmdir /s /q build dist
del *.spec

# Build the executable
pyinstaller --onefile --windowed --name "OrcaSlicer-Config-Manager" main.py
```

**Result:**
- Single executable file: `dist\OrcaSlicer-Config-Manager.exe`
- Completely standalone (no Python installation needed)
- Compatible with Windows 10+

---

## Important Notes

### Cross-Platform Building
- **macOS executables** can only be built on macOS systems
- **Windows executables** can only be built on Windows systems
- This is a PyInstaller limitation - it creates executables for the platform it runs on

### Distribution
- **macOS**: Distribute the entire `.app` bundle folder
- **Windows**: Distribute the single `.exe` file
- Both versions are completely self-contained with no external dependencies

### Compatibility
- **macOS**: Supports macOS 10.15+ (Intel and Apple Silicon)
- **Windows**: Supports Windows 10+
- Applications are approximately 13MB in size

### Troubleshooting
- If you get "application not supported" errors on Mac, ensure you built the executable on a Mac system
- If Windows Defender flags the executable, this is normal for PyInstaller builds - add an exception if needed
- Both build scripts will clean previous builds automatically

## Usage
Once built, simply run the application:
- **macOS**: Double-click the `.app` bundle
- **Windows**: Double-click the `.exe` file

The application provides a simple GUI for:
- Saving OrcaSlicer configuration backups
- Loading/restoring configurations
- Comparing current settings with saved backups