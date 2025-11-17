@echo off
REM AncesTree Installer for Windows
REM This script installs Docker Desktop and sets up AncesTree

echo ========================================
echo AncesTree Installer for Windows
echo ========================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script requires Administrator privileges
    echo.
    echo Please right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo Running as Administrator... OK
echo.

REM Check if Docker is already installed
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] Docker is already installed
    docker --version
    echo.
    goto :start_ancestree
)

echo [1/3] Docker not found. Installing Docker Desktop...
echo.

REM Create temp directory
set TEMP_DIR=%TEMP%\ancestree_install
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

echo Downloading Docker Desktop installer...
echo This may take several minutes (approximately 500 MB)...
echo.

REM Download Docker Desktop installer
powershell -Command "& {Invoke-WebRequest -Uri 'https://desktop.docker.com/win/main/amd64/Docker%%20Desktop%%20Installer.exe' -OutFile '%TEMP_DIR%\DockerDesktopInstaller.exe'}"

if %errorlevel% neq 0 (
    echo ERROR: Failed to download Docker Desktop
    echo.
    echo Please download manually from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Installing Docker Desktop...
echo.
echo IMPORTANT:
echo - The installer will open in a new window
echo - Follow the installation steps
echo - Leave all default options checked
echo - Click "Close" when installation completes
echo - DO NOT start Docker Desktop yet
echo.
pause

REM Run Docker Desktop installer
"%TEMP_DIR%\DockerDesktopInstaller.exe" install --quiet --accept-license

if %errorlevel% neq 0 (
    echo WARNING: Installer may have encountered issues
    echo Please check if Docker Desktop was installed
)

echo.
echo [3/3] Cleaning up...
del "%TEMP_DIR%\DockerDesktopInstaller.exe"
rmdir "%TEMP_DIR%"

echo.
echo ========================================
echo Docker Desktop Installation Complete!
echo ========================================
echo.
echo NEXT STEPS:
echo.
echo 1. RESTART YOUR COMPUTER (Important!)
echo.
echo 2. After restart, launch Docker Desktop from Start Menu
echo    - Wait for Docker to fully start (whale icon in system tray)
echo    - Accept any terms/conditions if prompted
echo.
echo 3. Run AncesTree:
echo    - Double-click: scripts\Start AncesTree.bat
echo    - Or run: python scripts\launcher.py
echo.
echo For help, see: docs\USER_GUIDE.md
echo.
pause
exit /b 0

:start_ancestree
echo Docker is installed and ready!
echo.
REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Desktop is not running.
    echo.
    echo Please start Docker Desktop and wait for it to be ready,
    echo then run: scripts\Start AncesTree.bat
    echo.
    pause
    exit /b 0
)

echo Would you like to start AncesTree now? (Y/N)
set /p START_NOW="> "

if /i "%START_NOW%"=="Y" (
    echo.
    echo Starting AncesTree...
    cd /d "%~dp0\.."
    python scripts\launcher.py
)

pause
