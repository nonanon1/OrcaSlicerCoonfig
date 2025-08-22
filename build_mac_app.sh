#!/bin/bash
echo "Building OrcaSlicer Configuration Manager for Mac with .app bundle and skull icon..."
echo

# Check if icon exists
if [ ! -f "skull_icon.icns" ]; then
    echo "WARNING: skull_icon.icns not found. Building without icon."
    echo "To add skull icon: Place skull_icon.icns file in this directory and run again."
    echo
    ICON_PARAM=""
else
    echo "Using skull_icon.icns"
    ICON_PARAM="--icon=skull_icon.icns"
fi

# Install PyInstaller if not already installed
pip3 install pyinstaller

# Build the .app bundle
pyinstaller --onefile --windowed --name "OrcaSlicer Config Manager" $ICON_PARAM main.py

# Create proper .app structure
APP_NAME="OrcaSlicer Config Manager.app"
if [ -f "dist/OrcaSlicer Config Manager" ]; then
    echo
    echo "Creating .app bundle..."
    
    # Create .app directory structure
    mkdir -p "dist/$APP_NAME/Contents/MacOS"
    mkdir -p "dist/$APP_NAME/Contents/Resources"
    
    # Move executable
    mv "dist/OrcaSlicer Config Manager" "dist/$APP_NAME/Contents/MacOS/"
    
    # Create Info.plist
    cat > "dist/$APP_NAME/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>OrcaSlicer Config Manager</string>
    <key>CFBundleIdentifier</key>
    <string>com.orcaslicer.configmanager</string>
    <key>CFBundleName</key>
    <string>OrcaSlicer Config Manager</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleIconFile</key>
    <string>skull_icon</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.9</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF
    
    # Copy icon if exists
    if [ -f "skull_icon.icns" ]; then
        cp "skull_icon.icns" "dist/$APP_NAME/Contents/Resources/"
    fi
    
    echo "✓ .app bundle created successfully!"
    echo "Location: dist/$APP_NAME"
    echo
    echo "You can now drag this .app to Applications folder or run directly."
else
    echo "Build failed - executable not found"
fi

echo
echo "Build complete!"