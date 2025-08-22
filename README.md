# OrcaSlicer Configuration Manager

A comprehensive GUI application for managing OrcaSlicer configurations with local and cloud backup capabilities. Features include configuration backup/restore, comparison tools, and seamless synchronization across devices using Google Drive and iCloud.

## Features

### 🔧 Core Configuration Management
- **Automatic Detection**: Finds OrcaSlicer installations and configurations across platforms
- **Complete Backup**: Saves all settings, printer profiles, and preferences in portable ZIP files
- **Easy Restore**: Restores configurations with progress tracking and validation
- **Smart Comparison**: Detailed diff tool showing exactly what changed between configurations

### ☁️ Cloud Storage Integration
- **Google Drive Sync**: Upload/download backups with OAuth2 authentication
- **iCloud Drive Support**: Native macOS iCloud integration for seamless device sync
- **Cross-Device Access**: Access your configurations from any authenticated device
- **Automatic Organization**: Creates dedicated cloud folders for backup management

### 🖥️ Cross-Platform Support
- **macOS**: Full native .app bundle with proper macOS integration
- **Windows**: Standalone .exe with comprehensive validation
- **Unified Experience**: Consistent interface and functionality across platforms

## 🆕 Latest Release Features

### ⚡ Revolutionary Build System
- **Zero Prerequisites**: No need to install Python, pip, or any dependencies manually
- **Automatic Everything**: Scripts handle Python installation, dependency resolution, and error recovery
- **Interactive Problem Solving**: Multiple solutions for any installation issue
- **Professional-Grade Automation**: Enterprise-level build reliability

### 🔧 Enhanced Dependency Management
- **Smart Detection**: Automatically finds and fixes Python/pip installation issues
- **Multiple Installation Strategies**: 5+ different methods to handle permission problems
- **Virtual Environment Support**: Isolated installations for maximum system safety
- **Graceful Fallbacks**: Cloud features degrade gracefully if dependencies unavailable

### 🛠️ Advanced Troubleshooting
- **Automatic Problem Resolution**: Interactive menus guide you through any build issues
- **Comprehensive Error Handling**: Clear solutions for every possible failure scenario
- **Real-time Diagnostics**: Build scripts provide detailed logging and status updates
- **Emergency Recovery**: Multiple backup strategies if standard installation fails

---

## Building the Application

This application can be built for both macOS and Windows as standalone executables. **No manual dependency installation required** - the enhanced build scripts handle everything automatically!

### 🍎 Building for macOS

**System Requirements:**
- macOS 10.15 or later
- Run on the target Mac system (Intel or Apple Silicon)
- ⚠️ **Python NOT required** - the build script can install it automatically!

**🔄 Automatic Dependency Resolution:**

The build script now handles **everything automatically**, including Python installation!

1. **Download/Clone the project files to your Mac**

2. **Open Terminal and navigate to the project folder:**
   ```bash
   cd path/to/OrcaSlicer-Config-Manager
   ```

3. **Run the intelligent build script:**
   ```bash
   chmod +x build_mac.sh
   ./build_mac.sh
   ```

**🚀 Automatic Python Installation:**
If Python is missing, the script offers:
- **Homebrew Installation** (recommended): Automatically installs Homebrew if needed, then Python
- **Manual Download**: Guides you through downloading from python.org
- **Interactive Setup**: Handles both Intel and Apple Silicon Macs automatically

**🛠️ Smart Permission Handling:**
When encountering permission issues, choose from:
1. **Standard Install**: Normal pip installation (recommended)
2. **User Directory**: Installs to your user folder (fixes "externally-managed-environment" errors)
3. **Virtual Environment**: Creates isolated environment (safest option)
4. **System Override**: Override package management (advanced users)
5. **Manual Installation**: Exit with guidance for manual setup

**🔧 Comprehensive Dependency Management:**
- **Automatic pip Installation**: Downloads and installs pip if missing
- **PATH Management**: Automatically updates PATH for Homebrew and user installations
- **Cloud Dependencies**: Installs Google Drive API libraries with fallback options
- **Module Validation**: Checks all required Python modules before building
- **Error Recovery**: Interactive problem-solving for any installation failures

**📦 Build Output:**
- Complete `.app` bundle: `dist/OrcaSlicer Configuration Manager.app`
- Full cloud storage integration included
- macOS-native executable with proper signing
- Ready for distribution or Applications folder installation
- Compatible with macOS 10.15+ (Universal: Intel and Apple Silicon)

---

### 🪟 Building for Windows

**System Requirements:**
- Windows 10 or later
- Must be run on a Windows system
- ⚠️ **Python NOT required** - the build script can install it automatically!

**🔄 Comprehensive Dependency Resolution:**

The Windows build script now handles **complete automatic setup**!

1. **Download/Extract the project files to your Windows machine**

2. **Open Command Prompt or PowerShell as Administrator (recommended) and navigate to the project folder:**
   ```cmd
   cd C:\path\to\OrcaSlicer-Config-Manager
   ```

3. **Run the intelligent build script:**
   ```cmd
   build_windows.bat
   ```

**🚀 Automatic Python Installation & Detection:**
If Python is missing or broken, the script provides:
1. **Automatic Download & Install**: Downloads Python 3.11 from python.org and installs silently
2. **PATH Detection & Repair**: Scans common Python installation locations and fixes PATH
3. **Manual Installation Guide**: Step-by-step instructions with exact download links
4. **Interactive Problem Solving**: Guides you through any installation issues

**🛠️ Advanced Permission Management:**
When encountering permission or installation issues:
- **Administrative Privileges**: Automatic elevation when needed
- **User Directory Installs**: Fallback to user-specific installations
- **Virtual Environment**: Creates isolated Python environment for maximum safety
- **Registry PATH Updates**: Automatically updates both system and user PATH variables

**🔧 Enhanced Dependency Management:**
- **Automatic pip Installation**: Downloads and installs pip if missing using get-pip.py
- **Cloud Dependencies**: Installs Google Drive API libraries with graceful fallbacks
- **PATH Refresh**: Dynamically updates PATH variables during installation
- **Comprehensive Validation**: Checks every installation step with clear error messages
- **Internet Connectivity**: Handles offline scenarios with appropriate guidance

**💾 PyInstaller Installation Strategies:**
When PyInstaller installation fails, choose from:
1. **User Directory Install**: Install to your user profile (no admin needed)
2. **Core-Only Install**: Install PyInstaller without cloud features
3. **Virtual Environment**: Isolated installation for system safety
4. **Manual Installation**: Exit with detailed guidance

**📦 Build Output:**
- Single executable file: `dist\OrcaSlicer-Config-Manager.exe`
- Full cloud storage integration included
- Completely standalone (no Python required on target machines)
- Built-in Windows validation and file size verification
- Compatible with Windows 10+ (x64 architecture)

---

## Usage

### 🚀 Getting Started

Once built, simply run the application:
- **macOS**: Double-click the `.app` bundle or drag to Applications folder
- **Windows**: Double-click the `.exe` file

### 📋 Core Operations

**Configuration Management:**
- **Save Configuration**: Creates timestamped ZIP backups of all OrcaSlicer settings
- **Load Configuration**: Restores configurations with progress tracking
- **Compare with Backup**: Detailed diff showing file changes, additions, and deletions

**Cloud Storage Features:**
- **Connect Cloud Storage**: Authenticate with Google Drive or iCloud Drive
- **Upload to Cloud**: Sync current configuration to your connected cloud service
- **Download from Cloud**: Retrieve backups from any connected device

### ☁️ Cloud Storage Setup

**Google Drive:**
1. Click "🔗 Connect Cloud Storage" 
2. Select Google Drive
3. Complete OAuth2 authentication in your browser
4. Automatically creates "OrcaSlicer Config Manager" folder

**iCloud Drive (macOS):**
1. Click "🔗 Connect Cloud Storage"
2. Select iCloud Drive  
3. Grants access to your iCloud Drive folder
4. Creates dedicated app folder for backups

**Cross-Device Synchronization:**
- Upload configurations from any device
- Download to any authenticated device
- Automatic conflict resolution
- Maintains backup history

## Important Notes

### 🔧 Build Requirements
- **macOS executables** can only be built on macOS systems
- **Windows executables** can only be built on Windows systems
- PyInstaller creates platform-specific executables

### 📦 Distribution
- **macOS**: Distribute the entire `.app` bundle folder
- **Windows**: Distribute the single `.exe` file
- Both versions are completely self-contained
- Cloud features work without additional setup

### 🔒 Security & Privacy
- Google Drive uses OAuth2 - no passwords stored
- iCloud uses local filesystem access
- All credentials stored locally and encrypted
- No data transmitted except to chosen cloud services

### ⚙️ Compatibility
- **macOS**: 10.15+ (Intel and Apple Silicon)
- **Windows**: Windows 10+
- **File Size**: ~13-15MB with cloud features
- **Dependencies**: None required on target machines

### 🛠️ Enhanced Troubleshooting & Problem Resolution

**🍎 macOS Build Issues:**

**Python Installation Problems:**
- **"Python not found"**: Script offers automatic Homebrew installation or manual download
- **"Externally-managed-environment"**: Choose "User directory install" from interactive menu
- **Homebrew permission errors**: Script handles sudo requirements automatically
- **PATH issues**: Automatic PATH updates for all installation methods

**Permission & Installation Errors:**
- **"pip install failed"**: Script provides 5 different installation strategies
- **"Permission denied"**: Try option 2 (User install) or option 3 (Virtual environment)
- **"Command not found"**: Script automatically detects and fixes PATH issues
- **Virtual environment failures**: Automatic cleanup and alternative method suggestions

**🪟 Windows Build Issues:**

**Python Installation & Detection:**
- **"Python is not installed"**: Script offers automatic download and installation
- **"Python not in PATH"**: Automatic detection of installed Python and PATH repair
- **Download failures**: Check internet connection, script provides manual installation guide
- **Installation requires admin**: Script attempts both admin and user installations

**Permission & Dependencies:**
- **"Access denied"**: Script tries user directory installation automatically
- **PyInstaller install fails**: Interactive menu with 4 different installation methods
- **PATH not updated**: Script refreshes PATH variables from registry automatically
- **Virtual environment errors**: Automatic cleanup and alternative suggestions

**🔧 Build Process Issues:**

**General Build Problems:**
- **"Build failed"**: Check console output for specific error, script provides detailed logging
- **"Executable not created"**: Validation step identifies missing files or corrupted builds
- **File size warnings**: Script analyzes executable size and suggests solutions
- **Cloud features unavailable**: Graceful fallback to core functionality

**📱 Cloud Storage Troubleshooting:**

**Authentication Issues:**
- **Google Drive connection fails**: Check internet connection, script provides re-authentication
- **iCloud not accessible**: Ensure iCloud Drive is enabled in System Preferences
- **Credentials lost**: Script handles re-authentication automatically
- **Permission errors**: Check cloud service settings and folder permissions

**Sync Problems:**
- **Upload failures**: Script provides detailed error messages and retry options
- **Download issues**: Verify cloud storage permissions and internet connectivity
- **File conflicts**: Built-in conflict resolution with user guidance

**🚨 Emergency Solutions:**

**Complete Failure Recovery:**
1. **Clean Installation**: Delete build directories and run script again
2. **Manual Python Setup**: Script provides exact download links and installation steps
3. **Minimal Build**: Install only PyInstaller for basic functionality
4. **System Reset**: Script can detect and repair most common system configuration issues

**Getting Help:**
- All error messages include specific solution suggestions
- Interactive menus guide you through problem resolution
- Build scripts include comprehensive logging for debugging
- Each failure provides multiple alternative approaches