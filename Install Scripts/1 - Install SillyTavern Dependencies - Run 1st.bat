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

:: Load NVM environment
echo Loading NVM environment...
CALL "%SystemDrive%\ProgramData\nvm\nvm.exe" use 18

:: Install Node.js
echo Installing Node.js...
choco install nodejs-lts -y

:skipInstallation
REM Navigate one directory up
cd..

echo Process completed successfully. Run "STSL GUI Launcher.bat" to relaunch the GUI and activate the installed requirements.

pause