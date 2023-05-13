@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Get the path of the parent folder
for %%I in ("%~dp0..\..") do set "ParentFolder=%%~fI"

:: Define the path to the SillyTavern directory
set "SillyTavernExtrasPath=%ParentFolder%\SillyTavern-extras"

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

REM Check if Python 3.10 is installed
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python 3.10 is not found. Installing Python 3.10 using Chocolatey...
    REM Install Python 3.10 using Chocolatey
    choco install python310 -y
)

REM Check if SillyTavern-extras is already installed
echo Checking if SillyTavern-extras is already installed...
if exist "%SillyTavernExtrasPath%" (
    echo SillyTavern-extras is already installed. Skipping clone...
) else (
    REM Clone the repository into the user's root folder
    echo Cloning the SillyTavernExtras...
    git clone https://github.com/Cohee1207/SillyTavern-extras "%SillyTavernExtrasPath%"
	
:: Check if InstallPaths.txt exists
if not exist "%~dp0..\InstallPaths.txt" (
    echo Creating InstallPaths.txt...
    echo SillyTavernExtras installed at: %SillyTavernExtrasPath% > "%~dp0..\InstallPaths.txt"
) else (
    echo Appending to InstallPaths.txt...
    echo SillyTavernExtras installed at: %SillyTavernExtrasPath% >> "%~dp0..\InstallPaths.txt"
)		
)

REM Check if the virtual environment with requirements is already created
echo Checking if the virtual environment with requirements is already created...
if exist "%SillyTavernExtrasPath%\venv" (
    echo Virtual environment with requirements is already created. Skipping virtual environment creation and package installation...
	
    REM Activate the virtual environment
    echo Activating the virtual environment...
    call "%SillyTavernExtrasPath%\venv\Scripts\activate.bat"
) else (
    REM Create the virtual environment
    echo Creating the virtual environment...
    python -m venv "%SillyTavernExtrasPath%\venv"

    REM Activate the virtual environment
    echo Activating the virtual environment...
    call "%SillyTavernExtrasPath%\venv\Scripts\activate.bat"

    REM Print the activated virtual environment
    echo Activated virtual environment: %VIRTUAL_ENV%

    REM Upgrade pip
    python -m pip install --upgrade pip

    REM Install the required packages within the virtual environment
    echo Installing required packages within the virtual environment...
    pip install -r "%SillyTavernExtrasPath%\requirements.txt"
)

REM Run the server
echo Starting the server...
start "" cmd /k "call "%SillyTavernExtrasPath%\venv\Scripts\activate.bat" && python "%SillyTavernExtrasPath%\server.py" --enable-modules=caption,summarize,classify"

pause
