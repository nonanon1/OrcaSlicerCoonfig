# OrcaSlicer Configuration Backup Tool

## Overview

This is a Python-based GUI application for managing OrcaSlicer configurations. The tool provides a simple graphical interface to backup, restore, and compare OrcaSlicer configuration files across different operating systems (Windows and macOS). The application automatically detects OrcaSlicer installations and configuration directories, allowing users to easily create portable backups of their printer profiles, settings, and preferences, plus compare current configurations with saved backups to see exactly what has changed.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Enhanced Application Architecture
The application follows a modular architecture with clear separation of concerns:

- **Entry Point**: `main.py` serves as the application launcher with argument parsing for different execution modes
- **Core Logic**: `orca_backup.py` contains the main backup and restore functionality
- **User Interfaces**: Single GUI interface with `gui.py` providing comprehensive graphical interaction
- **Utilities**: `utils.py` provides cross-platform path detection and file validation services
- **Cloud Integration**: `cloud_storage.py` provides Google Drive and iCloud synchronization capabilities

### Professional Build System with Dependency Resolution
The build scripts include sophisticated dependency management with multiple installation strategies:

#### macOS Build Features (`build_mac.sh`):
- **Automatic Python Installation**: Homebrew integration with fallback to manual installation
- **Interactive Installation Selection**: Multiple pip installation methods to handle permission issues
- **Virtual Environment Support**: Isolated dependency installation for system safety
- **Permission Handling**: User directory installs, system override options with warnings
- **PATH Management**: Automatic PATH updates for Homebrew and user installations

#### Windows Build Features (`build_windows.bat`):
- **Automatic Python Detection**: Scans common installation paths and fixes PATH issues
- **Download Integration**: Automatic Python installer download and silent installation
- **Permission Escalation**: Administrative privilege handling with user fallbacks
- **Multiple Installation Methods**: System, user, and virtual environment options
- **Registry Management**: PATH variable updates through system and user registry

### Cross-Platform Design
The system is designed to work across Windows, macOS, and Linux platforms by abstracting platform-specific path detection logic in the `OrcaSlicerPaths` utility class. This approach allows the core backup functionality to remain platform-agnostic while handling OS-specific configuration directory locations.

### Interface Architecture
The application implements a simple GUI-only interface:
- **GUI Interface**: Clean Tkinter-based graphical interface with three main functions: Save Configuration, Load Configuration, and Compare with Backup
- **Progress Feedback**: Real-time progress bar and status updates during operations
- **Configuration Comparison**: Detailed diff tool that shows exactly what files are different, added, or removed between current and saved configurations

### File Management Strategy
The backup system uses ZIP file format for configuration archives, providing compression and portability. The architecture includes file validation mechanisms to ensure backup integrity and proper error handling for various failure scenarios like missing installations or corrupted backups.

### Error Handling and Validation
The system implements comprehensive error handling through the `FileValidator` class and exception management in the core backup operations. This ensures graceful failure handling and informative error messages across both interface types.

## External Dependencies

### Core Dependencies
- **Python Standard Library**: The application primarily relies on built-in Python modules including `tkinter` for GUI, `zipfile` for archive handling, `pathlib` for cross-platform path management, and `argparse` for command-line parsing
- **Threading Module**: Used in the GUI interface for non-blocking operations during backup and restore processes
- **PyInstaller**: Used by build scripts to create standalone executables for distribution

### Cloud Storage Dependencies (Optional)
- **Google API Libraries**: For Google Drive integration with OAuth2 authentication
  - `google-api-python-client`: Google Drive API access
  - `google-auth-oauthlib`: OAuth2 authentication flow
  - `google-auth`: Core authentication library
- **Native Cloud Access**: iCloud Drive integration uses local filesystem access (macOS only)

### Target Application
- **OrcaSlicer**: The application is specifically designed to work with OrcaSlicer's configuration structure and file organization across different platforms

### Dependency Management Strategy
The application uses a hybrid approach to dependency management:
- **Core Features**: Built entirely with Python standard library for maximum portability
- **Cloud Features**: Optional external dependencies with graceful degradation when unavailable
- **Build Dependencies**: Automatically managed by enhanced build scripts with multiple installation strategies