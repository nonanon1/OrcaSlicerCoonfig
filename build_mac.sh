#!/bin/bash
echo "Building OrcaSlicer Configuration Manager for Mac..."
echo

# Install PyInstaller if not already installed
python -m pip install pyinstaller

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
echo "✅ Build complete!"
echo "📦 .app bundle created: dist/$APP_BUNDLE"
echo "🚀 You can now distribute the app bundle or drag it to Applications folder"
echo
echo "To test the app bundle:"
echo "  open \"dist/$APP_BUNDLE\""
echo
echo "To install in Applications:"
echo "  cp -r \"dist/$APP_BUNDLE\" /Applications/"