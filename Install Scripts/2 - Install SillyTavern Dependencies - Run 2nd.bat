@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

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

:: Check if Node.js is already installed
echo Checking if Node.js is installed...
node --version > nul 2>&1
if '%errorlevel%' EQU '0' (
    echo Node.js is already installed. Skipping installation.
    goto skipInstallation
)

:: Install Node.js
echo Installing Node.js...
nvm install 18
nvm use 18

:skipInstallation
echo Process completed successfully. Run "3a - Install SillyTavern - Main Branch.bat" to install the most stable recent release. Run "3b - Install SillyTavern - Developer Preview Branch" to install the latest developer preview.
pause
