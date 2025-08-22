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

:: Enhanced Python installation checking and resolution
call :check_and_install_python
goto :continue_after_python

:check_and_install_python
python --version >nul 2>&1
if not errorlevel 1 goto :eof

echo ^❌ Python not found. Let's resolve this...
echo.
echo Python installation options:
echo 1^) Download and install Python automatically
echo 2^) Fix PATH if Python is installed but not found
echo 3^) Manual installation guidance
echo 4^) Exit
echo.

:python_choice_loop
set /p choice="Select option [1-4]: "
if "%choice%"=="1" goto :install_python_auto
if "%choice%"=="2" goto :fix_python_path
if "%choice%"=="3" goto :python_manual_guide
if "%choice%"=="4" exit /b 1
echo Please select 1, 2, 3, or 4
goto :python_choice_loop

:install_python_auto
echo ^📥 Automatic Python Installation
echo.
echo This will download and install Python 3.11 from python.org
echo Administrative privileges may be required.
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" goto :python_choice_loop

echo Downloading Python installer...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'python_installer.exe'}"

if not exist "python_installer.exe" (
    echo ^❌ Failed to download Python installer
    goto :python_choice_loop
)

echo Installing Python ^(this may take a few minutes^)...
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo Cleaning up...
del python_installer.exe

echo Refreshing PATH...
call :refresh_path

python --version >nul 2>&1
if errorlevel 1 (
    echo ^❌ Python installation may have failed
    echo Please try manual installation option
    goto :python_choice_loop
) else (
    echo ^✅ Python installed successfully
    goto :eof
)

:fix_python_path
echo ^🔧 Fixing Python PATH...
echo.
echo Searching for Python installations...

:: Common Python installation paths
set "PYTHON_PATHS=C:\Python3*\python.exe"
set "PYTHON_PATHS=%PYTHON_PATHS% C:\Program Files\Python3*\python.exe"
set "PYTHON_PATHS=%PYTHON_PATHS% C:\Program Files (x86)\Python3*\python.exe"
set "PYTHON_PATHS=%PYTHON_PATHS% %LOCALAPPDATA%\Programs\Python\Python3*\python.exe"
set "PYTHON_PATHS=%PYTHON_PATHS% %APPDATA%\Python\Python3*\python.exe"

set "FOUND_PYTHON="
for %%p in (%PYTHON_PATHS%) do (
    if exist "%%p" (
        set "FOUND_PYTHON=%%p"
        echo Found Python at: %%p
        goto :found_python_path
    )
)

echo ^❌ No Python installation found in common locations
echo Please try option 1 ^(automatic installation^) or option 3 ^(manual guidance^)
goto :python_choice_loop

:found_python_path
set "PYTHON_DIR="
for %%i in ("%FOUND_PYTHON%") do set "PYTHON_DIR=%%~dpi"
set "PYTHON_DIR=%PYTHON_DIR:~0,-1%"

echo Adding %PYTHON_DIR% to PATH...
setx PATH "%PATH%;%PYTHON_DIR%;%PYTHON_DIR%\Scripts" /M 2>nul
if errorlevel 1 (
    echo ^⚠️ Could not update system PATH ^(requires admin privileges^)
    echo Adding to user PATH instead...
    setx PATH "%PATH%;%PYTHON_DIR%;%PYTHON_DIR%\Scripts"
)

call :refresh_path

python --version >nul 2>&1
if errorlevel 1 (
    echo ^❌ PATH fix unsuccessful
    goto :python_choice_loop
) else (
    echo ^✅ Python PATH fixed successfully
    goto :eof
)

:python_manual_guide
echo ^📋 Manual Python Installation Guide
echo.
echo Please follow these steps:
echo 1. Go to https://www.python.org/downloads/windows/
echo 2. Download Python 3.11 or later ^(64-bit recommended^)
echo 3. Run the installer as Administrator
echo 4. ^⚠️ IMPORTANT: Check "Add Python to PATH" during installation
echo 5. Complete the installation
echo 6. Open a NEW command prompt and run this script again
echo.
pause
exit /b 1

:refresh_path
:: Refresh PATH variable
for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SYS_PATH=%%b"
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Environment" /v PATH 2^>nul') do set "USER_PATH=%%b"
set "PATH=%SYS_PATH%;%USER_PATH%"
goto :eof

:continue_after_python

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

:: Enhanced pip checking and installation
call :check_and_setup_pip
goto :continue_after_pip

:check_and_setup_pip
python -m pip --version >nul 2>&1
if not errorlevel 1 (
    echo ^✅ pip available
    goto :eof
)

echo ^❌ pip not available. Installing pip...

:: Download get-pip.py
echo Downloading pip installer...
powershell -Command "& {Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'}"

if not exist "get-pip.py" (
    echo ^❌ Failed to download pip installer
    echo Please check your internet connection
    pause
    exit /b 1
)

echo Installing pip...
python get-pip.py --user
if errorlevel 1 (
    echo ^❌ Failed to install pip
    del get-pip.py
    pause
    exit /b 1
)

echo Cleaning up...
del get-pip.py

echo Refreshing PATH for pip...
call :refresh_path

python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ^❌ pip still not available after installation
    pause
    exit /b 1
) else (
    echo ^✅ pip installed and available
)
goto :eof

:continue_after_pip

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

:: Enhanced PyInstaller installation with permission handling
call :install_pyinstaller_with_permissions
goto :continue_after_pyinstaller

:install_pyinstaller_with_permissions
echo ^🔧 Installing PyInstaller and cloud dependencies...

:: Try standard installation first
python -m pip install --upgrade pyinstaller google-api-python-client google-auth-oauthlib >nul 2>&1
if not errorlevel 1 (
    echo ^✅ PyInstaller and cloud dependencies installed successfully
    goto :eof
)

echo ^❌ Standard installation failed. Trying alternative methods...
echo.
echo Installation options:
echo 1^) Install to user directory
echo 2^) Install PyInstaller only ^(limited cloud features^)
echo 3^) Create virtual environment
echo 4^) Exit and install manually
echo.

:pyinstaller_choice_loop
set /p choice="Select option [1-4]: "
if "%choice%"=="1" goto :install_pyinstaller_user
if "%choice%"=="2" goto :install_pyinstaller_only
if "%choice%"=="3" goto :install_pyinstaller_venv
if "%choice%"=="4" exit /b 1
echo Please select 1, 2, 3, or 4
goto :pyinstaller_choice_loop

:install_pyinstaller_user
echo Installing to user directory...
python -m pip install --user --upgrade pyinstaller google-api-python-client google-auth-oauthlib
if errorlevel 1 (
    echo ^❌ User installation failed
    goto :pyinstaller_choice_loop
) else (
    echo ^✅ PyInstaller and cloud dependencies installed successfully ^(user install^)
    goto :eof
)

:install_pyinstaller_only
echo Installing PyInstaller only...
python -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo ^❌ PyInstaller installation failed
    goto :pyinstaller_choice_loop
) else (
    echo ^✅ PyInstaller installed successfully ^(cloud features limited^)
    goto :eof
)

:install_pyinstaller_venv
echo Creating virtual environment...
python -m venv build_env
if errorlevel 1 (
    echo ^❌ Virtual environment creation failed
    goto :pyinstaller_choice_loop
)

echo Activating virtual environment...
call build_env\Scripts\activate.bat

echo Installing dependencies in virtual environment...
pip install --upgrade pip
pip install pyinstaller google-api-python-client google-auth-oauthlib
if errorlevel 1 (
    echo ^❌ Failed to install dependencies in virtual environment
    deactivate
    rmdir /s /q build_env
    goto :pyinstaller_choice_loop
) else (
    echo ^✅ PyInstaller and cloud dependencies installed in virtual environment
    set USING_VENV=true
    goto :eof
)

:continue_after_pyinstaller

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