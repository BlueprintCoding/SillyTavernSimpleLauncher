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

REM Check if SillyTavern-extras is installed
echo Checking if SillyTavern-extras is installed...
if exist "%ParentFolder%\SillyTavern-extras" (
    REM Deactivate and remove the virtual environment
    echo Deactivating and removing the virtual environment...
    call "%ParentFolder%\SillyTavern-extras\venv\Scripts\deactivate.bat"
    rmdir /s /q "%ParentFolder%\SillyTavern-extras\venv"

    REM Remove the SillyTavern-extras folder
    echo Removing the SillyTavern-extras folder...
    rmdir /s /q "%ParentFolder%\SillyTavern-extras"

    echo SillyTavern-extras is uninstalled successfully.
) else (
    echo SillyTavern-extras is not installed.
)

pause
