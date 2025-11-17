@echo off
REM Windows launcher for AncesTree
REM This file can be double-clicked to start AncesTree

REM Change to project root (parent of scripts directory)
cd /d "%~dp0\.."

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python 3 from https://www.python.org
    pause
    exit /b 1
)

REM Start launcher
python scripts\launcher.py

pause
