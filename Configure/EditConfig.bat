@echo off
setlocal enabledelayedexpansion

:: Check if Chocolatey is already installed
choco -v >nul 2>&1
if %errorlevel% equ 0 (
    echo Chocolatey is already installed.
) else (
    echo Installing Chocolatey...
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
)

REM Check if Python 3.10 is installed
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python 3.10 is not found. Installing Python 3.10 using Chocolatey...
    REM Install Python 3.10 using Chocolatey
    choco install python310 -y
)

:: Check if Tkinter is already installed
python -c "import tkinter" >nul 2>&1
if %errorlevel% equ 0 (
    echo Tkinter is already installed.
) else (
    echo Installing Tkinter...
    python -m pip install tkinter
)

REM Launch the EditConfig.py GUI script
python "%~dp0EditConfig.py"

REM Prompt the user for input to keep the window open
pause

REM End of the script

endlocal
exit
