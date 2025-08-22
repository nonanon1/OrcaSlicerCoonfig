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

## Building the Application

This application can be built for both macOS and Windows as standalone executables that don't require Python to be installed.

### 🍎 Building for macOS

**Requirements:**
- macOS 10.15 or later
- Python 3.7+ installed
- Run on the target Mac system (Intel or Apple Silicon)

**Enhanced Build Process:**

1. **Download/Clone the project files to your Mac**

2. **Open Terminal and navigate to the project folder:**
   ```bash
   cd path/to/OrcaSlicer-Config-Manager
   ```

3. **Run the enhanced build script:**
   ```bash
   chmod +x build_mac.sh
   ./build_mac.sh
   ```

**Interactive Build Features:**
- **Smart Dependency Checking**: Verifies Python version, pip, and required modules before building
- **Installation Strategy Selection**: Choose from multiple installation methods if you encounter permission issues:
  - Standard install (recommended)
  - User directory install (fixes externally-managed-environment errors)
  - Virtual environment (safest approach)
  - System override (with confirmation)
- **Comprehensive Validation**: Post-build verification ensures your .app bundle is complete and functional

**What Gets Installed:**
- PyInstaller for building executables
- Google Drive API libraries for cloud sync (optional)
- OAuth2 authentication libraries

**Result:**
- Complete `.app` bundle: `dist/OrcaSlicer Configuration Manager.app`
- Full cloud storage integration included
- Ready for distribution or Applications folder installation
- Works on macOS 10.15+ (Intel and Apple Silicon compatible)

---

### 🪟 Building for Windows

**Requirements:**
- Windows 10 or later  
- Python 3.7+ installed
- Must be run on a Windows system

**Enhanced Build Process:**

1. **Download/Extract the project files to your Windows machine**

2. **Open Command Prompt or PowerShell and navigate to the project folder:**
   ```cmd
   cd C:\path\to\OrcaSlicer-Config-Manager
   ```

3. **Run the enhanced build script:**
   ```cmd
   build_windows.bat
   ```

**Comprehensive Build Features:**
- **Full System Validation**: Checks Windows environment, Python version, pip, and all required modules
- **Smart Dependency Installation**: Installs PyInstaller and cloud storage libraries with fallback options
- **Real-time Progress**: Shows detailed build progress with error handling
- **Executable Validation**: Post-build verification ensures the .exe is properly created and functional
- **File Size Analysis**: Warns if executable size seems incorrect

**What Gets Installed:**
- PyInstaller for building executables
- Google Drive API libraries for cloud synchronization
- OAuth2 authentication support

**Result:**
- Single executable file: `dist\OrcaSlicer-Config-Manager.exe`
- Full cloud storage integration included
- Completely standalone (no Python installation needed on target machines)
- Compatible with Windows 10+

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

### 🛠️ Troubleshooting

**macOS Issues:**
- "Application not supported": Build on actual Mac system
- "Externally-managed-environment": Use build script's interactive installer selection
- Permission errors: Try user directory installation option

**Windows Issues:**
- Windows Defender warnings: Normal for PyInstaller builds, add exception
- PATH issues: Build script includes Python PATH verification
- Missing modules: Comprehensive dependency checking prevents build failures

**Cloud Storage Issues:**
- Google Drive: Requires internet connection for initial setup
- iCloud: Ensure iCloud Drive is enabled in System Preferences
- Authentication: Stored locally, re-authenticate if issues persist