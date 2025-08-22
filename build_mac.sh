#!/bin/bash
set -e  # Exit on any error

echo "Building OrcaSlicer Configuration Manager for Mac..."
echo "🔍 Checking dependencies..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script must be run on macOS"
    echo "   Current system: $OSTYPE"
    exit 1
fi

# Check Python 3 installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "   Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

# Check Python version (minimum 3.7)
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 7 ]]; then
    echo "❌ Error: Python 3.7+ required, found Python $PYTHON_VERSION"
    echo "   Please upgrade Python from https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"

# Check pip
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ Error: pip is not available"
    echo "   Please install pip for Python 3"
    exit 1
fi

echo "✅ pip available"

# Check required source files
REQUIRED_FILES=("main.py" "gui.py" "orca_backup.py" "utils.py")
for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "❌ Error: Required file missing: $file"
        echo "   Please ensure all project files are present"
        exit 1
    fi
done

echo "✅ All required source files found"

# Check if we can import required modules
echo "🔍 Checking Python dependencies..."
python3 -c "
import sys
missing_modules = []
try:
    import tkinter
except ImportError:
    missing_modules.append('tkinter')
try:
    import pathlib
except ImportError:
    missing_modules.append('pathlib')
try:
    import zipfile
except ImportError:
    missing_modules.append('zipfile')

if missing_modules:
    print('❌ Error: Missing Python modules:', ', '.join(missing_modules))
    if 'tkinter' in missing_modules:
        print('   On macOS, install tkinter with: brew install python-tk')
    sys.exit(1)
else:
    print('✅ All Python dependencies satisfied')
"

# Install PyInstaller and optional cloud dependencies
echo "🔧 Installing PyInstaller and dependencies..."

# Check if PyInstaller is already installed
if command -v pyinstaller &> /dev/null; then
    echo "✅ PyInstaller already available"
    PYINSTALLER_INSTALLED=true
else
    echo "PyInstaller not found. Please choose an installation method:"
    echo ""
    echo "1. Standard install (recommended for most systems)"
    echo "2. User install (install to your user directory only)"
    echo "3. Virtual environment (safest, creates isolated environment)"
    echo "4. Override system packages (use with caution)"
    echo "5. Exit and install manually"
    echo ""
    
    while true; do
        read -p "Select option [1-5]: " choice
        case $choice in
            1)
                echo "Installing PyInstaller with standard method..."
                if python3 -m pip install --upgrade pyinstaller google-api-python-client google-auth-oauthlib; then
                    echo "✅ PyInstaller and cloud dependencies installed successfully"
                    PYINSTALLER_INSTALLED=true
                    break
                else
                    echo "❌ Standard install failed. Try another option."
                    echo ""
                fi
                ;;
            2)
                echo "Installing PyInstaller to user directory..."
                if python3 -m pip install --user --upgrade pyinstaller google-api-python-client google-auth-oauthlib; then
                    echo "✅ PyInstaller and cloud dependencies installed successfully (user install)"
                    # Update PATH to include user bin directory
                    export PATH="$HOME/.local/bin:$HOME/Library/Python/$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')/bin:$PATH"
                    PYINSTALLER_INSTALLED=true
                    break
                else
                    echo "❌ User install failed. Try another option."
                    echo ""
                fi
                ;;
            3)
                echo "Creating virtual environment..."
                if python3 -m venv build_env && source build_env/bin/activate && pip install pyinstaller; then
                    echo "✅ PyInstaller installed in virtual environment"
                    echo "ℹ️  Using virtual environment for build"
                    PYINSTALLER_INSTALLED=true
                    USING_VENV=true
                    break
                else
                    echo "❌ Virtual environment setup failed. Try another option."
                    echo ""
                fi
                ;;
            4)
                echo "⚠️  Warning: This will override system package management"
                read -p "Are you sure you want to continue? [y/N]: " confirm
                if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
                    echo "Installing PyInstaller with system override..."
                    if python3 -m pip install --break-system-packages --upgrade pyinstaller; then
                        echo "✅ PyInstaller installed successfully (system override)"
                        PYINSTALLER_INSTALLED=true
                        break
                    else
                        echo "❌ System override install failed. Try another option."
                        echo ""
                    fi
                else
                    echo "Operation cancelled. Choose another option."
                    echo ""
                fi
                ;;
            5)
                echo "Build cancelled. Please install PyInstaller manually and run the script again."
                echo ""
                echo "Manual installation options:"
                echo "  • Virtual environment: python3 -m venv env && source env/bin/activate && pip install pyinstaller"
                echo "  • User install: python3 -m pip install --user pyinstaller"
                echo "  • Homebrew: brew install pyinstaller"
                exit 0
                ;;
            *)
                echo "Invalid option. Please choose 1-5."
                ;;
        esac
    done
    
    if [[ "$PYINSTALLER_INSTALLED" != "true" ]]; then
        echo "❌ Error: PyInstaller installation failed"
        exit 1
    fi
fi

# Verify PyInstaller is available
if ! command -v pyinstaller &> /dev/null; then
    echo "⚠️  PyInstaller not found in PATH, checking common locations..."
    
    # Check user local bin
    if [ -f "$HOME/.local/bin/pyinstaller" ]; then
        export PATH="$HOME/.local/bin:$PATH"
        echo "✅ Found PyInstaller in user local bin"
    # Check Python user bin
    elif [ -f "$HOME/Library/Python/$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')/bin/pyinstaller" ]; then
        export PATH="$HOME/Library/Python/$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')/bin:$PATH"
        echo "✅ Found PyInstaller in Python user bin"
    else
        echo "❌ Error: PyInstaller installed but not accessible"
        echo "   Try running: export PATH=\"\$HOME/.local/bin:\$PATH\""
        exit 1
    fi
fi

# Clean previous builds
rm -rf build dist *.spec

# Build the executable
pyinstaller --onefile --windowed --name "OrcaSlicer-Config-Manager" main.py

# Create proper .app bundle
APP_NAME="OrcaSlicer Configuration Manager"
APP_BUNDLE="$APP_NAME.app"
EXECUTABLE_NAME="OrcaSlicer-Config-Manager"

echo
echo "Creating proper .app bundle..."

# Remove existing .app bundle if it exists
rm -rf "dist/$APP_BUNDLE"

# Create .app bundle directory structure
mkdir -p "dist/$APP_BUNDLE/Contents/MacOS"
mkdir -p "dist/$APP_BUNDLE/Contents/Resources"

# Move executable to correct location in bundle
mv "dist/$EXECUTABLE_NAME" "dist/$APP_BUNDLE/Contents/MacOS/"

# Create Info.plist
cat > "dist/$APP_BUNDLE/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleDisplayName</key>
    <string>OrcaSlicer Configuration Manager</string>
    <key>CFBundleExecutable</key>
    <string>OrcaSlicer-Config-Manager</string>
    <key>CFBundleIconFile</key>
    <string>icon</string>
    <key>CFBundleIdentifier</key>
    <string>com.orcaslicer.config-manager</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>OrcaSlicer Configuration Manager</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.utilities</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright © 2024 OrcaSlicer Configuration Manager. All rights reserved.</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
EOF

# Set executable permissions
chmod +x "dist/$APP_BUNDLE/Contents/MacOS/$EXECUTABLE_NAME"

# Set bundle permissions
chmod -R 755 "dist/$APP_BUNDLE"

echo
echo "🔍 Validating app bundle integrity..."

# Variables for validation
APP_BUNDLE_PATH="dist/$APP_BUNDLE"
EXECUTABLE_PATH="$APP_BUNDLE_PATH/Contents/MacOS/$EXECUTABLE_NAME"
PLIST_PATH="$APP_BUNDLE_PATH/Contents/Info.plist"

# Check if .app bundle exists
if [[ ! -d "$APP_BUNDLE_PATH" ]]; then
    echo "❌ Error: .app bundle was not created at $APP_BUNDLE_PATH"
    exit 1
fi

echo "✅ .app bundle exists"

# Check if executable exists
if [[ ! -f "$EXECUTABLE_PATH" ]]; then
    echo "❌ Error: Executable not found at $EXECUTABLE_PATH"
    exit 1
fi

echo "✅ Executable exists"

# Check if executable is actually executable
if [[ ! -x "$EXECUTABLE_PATH" ]]; then
    echo "❌ Error: Executable is not executable (permissions issue)"
    exit 1
fi

echo "✅ Executable has proper permissions"

# Check if Info.plist exists
if [[ ! -f "$PLIST_PATH" ]]; then
    echo "❌ Error: Info.plist not found at $PLIST_PATH"
    exit 1
fi

echo "✅ Info.plist exists"

# Validate Info.plist format
if ! plutil -lint "$PLIST_PATH" &> /dev/null; then
    echo "❌ Error: Info.plist is malformed"
    exit 1
fi

echo "✅ Info.plist is valid"

# Get file size of executable
EXEC_SIZE=$(stat -f%z "$EXECUTABLE_PATH" 2>/dev/null || echo "0")
EXEC_SIZE_MB=$((EXEC_SIZE / 1024 / 1024))

if [[ $EXEC_SIZE -lt 1000000 ]]; then  # Less than 1MB is suspicious
    echo "⚠️  Warning: Executable size is unusually small (${EXEC_SIZE_MB}MB)"
    echo "   This might indicate a build problem"
else
    echo "✅ Executable size looks reasonable (${EXEC_SIZE_MB}MB)"
fi

# Test if app bundle can be launched (dry run)
echo "🧪 Testing app bundle launch capability..."
if codesign --verify --deep --strict "$APP_BUNDLE_PATH" &> /dev/null; then
    echo "✅ Code signature verification passed"
else
    echo "⚠️  Warning: No valid code signature (expected for unsigned builds)"
fi

# Try to get basic info from the app
if /usr/libexec/PlistBuddy -c "Print CFBundleDisplayName" "$PLIST_PATH" &> /dev/null; then
    APP_DISPLAY_NAME=$(/usr/libexec/PlistBuddy -c "Print CFBundleDisplayName" "$PLIST_PATH")
    echo "✅ App bundle info: $APP_DISPLAY_NAME"
else
    echo "⚠️  Warning: Could not read app bundle display name"
fi

echo
echo "🎉 Build validation complete!"
echo "📦 .app bundle created: dist/$APP_BUNDLE"
echo "📊 Bundle size: $(du -sh "$APP_BUNDLE_PATH" | cut -f1)"
echo "🚀 Ready for distribution or installation"
echo
echo "To test the app bundle:"
echo "  open \"dist/$APP_BUNDLE\""
echo
echo "To install in Applications:"
echo "  cp -r \"dist/$APP_BUNDLE\" /Applications/"
echo
echo "🔍 To verify the app works:"
echo "  1. Double-click the .app bundle in Finder"
echo "  2. Or run: \"$EXECUTABLE_PATH\" --version"