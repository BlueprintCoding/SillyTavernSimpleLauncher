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

    REM Install the required packages from requirements.txt
    echo Installing required packages...
    pip install --no-cache-dir -r "%SillyTavernExtrasPath%\requirements.txt"
)

REM Prompt user to select modules to enable
echo Available modules:
echo 1: caption
echo 2: summarize
echo 3: classify
echo 4: keywords
echo 5: prompt
echo 6: sd
echo 7: tts
echo If no value is provided, caption, summarize, and classify will load by default.
set /p "moduleSelection=Enter the module numbers to enable (separated by spaces ex: 1 2 5): "

REM Set default modules if no selection is made or incorrect input
set "enabledModules=caption,summarize,classify"
set "moduleMap[1]=caption"
set "moduleMap[2]=summarize"
set "moduleMap[3]=classify"
set "moduleMap[4]=keywords"
set "moduleMap[5]=prompt"
set "moduleMap[6]=sd"
set "moduleMap[7]=tts"

for %%m in (%moduleSelection%) do (
    set "module=!moduleMap[%%m]!"
    if defined module (
        set "enabledModules=!enabledModules!,!module!"
    )
)

REM Run the server with enabled modules
echo Starting the server...
start "" /B cmd /C "call "%SillyTavernExtrasPath%\venv\Scripts\activate.bat" && python "%SillyTavernExtrasPath%\server.py" --enable-modules=%enabledModules%"

pause
