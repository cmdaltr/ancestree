@echo off
REM Build script for Windows executable
REM Run this on a Windows machine to create Ancestree.exe

echo ========================================
echo Building Ancestree for Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/5] Installing build dependencies...
pip install -r build_requirements.txt

echo.
echo [2/5] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Ancestree.exe del Ancestree.exe

echo.
echo [3/5] Building executable with PyInstaller...
pyinstaller --clean --noconfirm ancestree.spec

echo.
echo [4/5] Copying executable to root directory...
if exist dist\Ancestree.exe (
    copy dist\Ancestree.exe Ancestree.exe
    echo Success! Executable created: Ancestree.exe
) else (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo [5/5] Creating installer package...
echo Note: For a proper installer, consider using Inno Setup or NSIS
echo Download Inno Setup from: https://jrsoftware.org/isinfo.php

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable: Ancestree.exe
echo Size:
for %%A in (Ancestree.exe) do echo %%~zA bytes
echo.
echo You can now distribute Ancestree.exe to Windows users.
echo They will need Docker Desktop installed to run it.
echo.
pause
