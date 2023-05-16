@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Get the path of the parent folder
for %%I in ("%~dp0..\..") do set "ParentFolder=%%~fI"

:: Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

REM Option 2 - Vanilla

:: Check if Chocolatey is already installed
choco -v >nul 2>&1
if %errorlevel% equ 0 (
    echo Chocolatey is already installed.
) else (
    echo Chocolatey is not installed, run the "RUN FIRST Install GUI Dependencies.bat".
)

:: Check if Git is already installed
git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Git is already installed.
) else (
    echo Git is not installed, run the "RUN FIRST Install GUI Dependencies.bat".
)

:: Check if NVM is already installed
nvm version >nul 2>&1
if %errorlevel% equ 0 (
    echo NVM is already installed.
) else (
    echo NVM is not installed, run the "RUN FIRST Install GUI Dependencies.bat".
)


REM Check if Python 3.10 is installed
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python 3.10 is not found. Installing Python 3.10 using Chocolatey...
    REM Install Python 3.10 using Chocolatey
    choco install python310 -y
)

:: Check if Pillow is already installed
python -c "import PIL" >nul 2>&1
if %errorlevel% equ 0 (
    echo Pillow is already installed.
) else (
	echo Pillow is not installed, run the "RUN FIRST Install GUI Dependencies.bat".
)

:: Check if Tkinter is already installed
python -c "import tkinter" >nul 2>&1
if %errorlevel% equ 0 (
    echo Tkinter is already installed.
) else (
    echo Tkinter is not installed, run the "RUN FIRST Install GUI Dependencies.bat".
)

:: Check if pywin32 is installed
python -c "import win32api" >nul 2>&1
if %errorlevel% equ 0 (
    echo pywin32 is already installed.
) else (
    echo pywin32 is not installed, run the "RUN FIRST Install GUI Dependencies.bat".
)

REM Launch the "STLauncherGui.py" GUI
start "" python STLauncherGui.py

REM Close the command window after a successful install or check
exit
