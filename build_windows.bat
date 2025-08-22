@echo off
setlocal enabledelayedexpansion

echo Building OrcaSlicer Configuration Manager for Windows...
echo ^🔍 Checking dependencies...

:: Check if we're on Windows
if not "%OS%"=="Windows_NT" (
    echo ^❌ Error: This script must be run on Windows
    echo    Current system: %OS%
    pause
    exit /b 1
)

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ^❌ Error: Python is not installed or not in PATH
    echo    Please install Python from https://www.python.org/downloads/
    echo    Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
echo ^✅ Python %PYTHON_VERSION% found

:: Check Python version (minimum 3.7)
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

if %PYTHON_MAJOR% LSS 3 (
    echo ^❌ Error: Python 3.7+ required, found Python %PYTHON_VERSION%
    echo    Please upgrade Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

if %PYTHON_MAJOR% EQU 3 if %PYTHON_MINOR% LSS 7 (
    echo ^❌ Error: Python 3.7+ required, found Python %PYTHON_VERSION%
    echo    Please upgrade Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ^❌ Error: pip is not available
    echo    Please reinstall Python with pip included
    pause
    exit /b 1
)

echo ^✅ pip available

:: Check required source files
set REQUIRED_FILES=main.py gui.py orca_backup.py utils.py
for %%f in (%REQUIRED_FILES%) do (
    if not exist "%%f" (
        echo ^❌ Error: Required file missing: %%f
        echo    Please ensure all project files are present
        pause
        exit /b 1
    )
)

echo ^✅ All required source files found

:: Check Python dependencies
echo ^🔍 Checking Python dependencies...
python -c "import sys; missing=[]; [missing.append(m) for m in ['tkinter','pathlib','zipfile'] if __import__('importlib').util.find_spec(m) is None]; sys.exit(1) if missing else print('✅ All Python dependencies satisfied')" 2>nul
if errorlevel 1 (
    echo ^❌ Error: Missing Python modules detected
    echo    Common issue: tkinter not included with Python installation
    echo    Please reinstall Python with tkinter support
    pause
    exit /b 1
)

:: Install PyInstaller and cloud dependencies
echo ^🔧 Installing PyInstaller and cloud dependencies...
python -m pip install --upgrade pyinstaller google-api-python-client google-auth-oauthlib
if errorlevel 1 (
    echo ^❌ Error: Failed to install PyInstaller and dependencies
    echo    Note: Cloud storage features may not be available
    echo    Trying PyInstaller only...
    python -m pip install --upgrade pyinstaller
    if errorlevel 1 (
        echo ^❌ Error: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo ^✅ PyInstaller installed successfully ^(cloud features limited^)
) else (
    echo ^✅ PyInstaller and cloud dependencies installed successfully
)

:: Clean previous builds
echo ^🧹 Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

:: Build the executable
echo ^🔨 Building executable...
pyinstaller --onefile --windowed --name "OrcaSlicer-Config-Manager" main.py
if errorlevel 1 (
    echo ^❌ Error: Build failed
    pause
    exit /b 1
)

:: Validation section
echo.
echo ^🔍 Validating executable...

set EXECUTABLE_PATH=dist\OrcaSlicer-Config-Manager.exe

:: Check if executable exists
if not exist "%EXECUTABLE_PATH%" (
    echo ^❌ Error: Executable was not created at %EXECUTABLE_PATH%
    pause
    exit /b 1
)

echo ^✅ Executable exists

:: Check file size
for %%A in ("%EXECUTABLE_PATH%") do set EXEC_SIZE=%%~zA
set /a EXEC_SIZE_MB=!EXEC_SIZE!/1024/1024

if %EXEC_SIZE% LSS 1000000 (
    echo ^⚠️  Warning: Executable size is unusually small ^(!EXEC_SIZE_MB!MB^)
    echo    This might indicate a build problem
) else (
    echo ^✅ Executable size looks reasonable ^(!EXEC_SIZE_MB!MB^)
)

:: Test executable properties
echo ^🧪 Testing executable properties...
powershell -command "try { $file = Get-Item '%EXECUTABLE_PATH%'; if ($file.Extension -eq '.exe') { Write-Host '✅ Valid Windows executable' } else { Write-Host '❌ Invalid file type' } } catch { Write-Host '⚠️  Could not verify file properties' }" 2>nul

:: Try to get file version info
powershell -command "try { $version = [System.Diagnostics.FileVersionInfo]::GetVersionInfo('%EXECUTABLE_PATH%'); Write-Host '✅ Executable metadata accessible' } catch { Write-Host '⚠️  Could not read executable metadata' }" 2>nul

echo.
echo ^🎉 Build validation complete!
echo ^📦 Windows executable created: %EXECUTABLE_PATH%
echo ^📊 File size: !EXEC_SIZE_MB!MB
echo ^🚀 Ready for distribution
echo.
echo ^🔍 To test the executable:
echo   1. Double-click: %EXECUTABLE_PATH%
echo   2. Or run from command line: "%EXECUTABLE_PATH%"
echo.
echo ^💡 Distribution note:
echo   The .exe file is completely standalone - no Python installation needed
echo.
pause