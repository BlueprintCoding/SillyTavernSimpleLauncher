@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
:: Add PowerShell to PATH
set PATH=%SYSTEMROOT%\system32\WindowsPowerShell\v1.0\;%PATH%

:: Set the path of the parent folder
for %%I in ("%~dp0....") do set "ParentFolder=%%~fI"

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

REM Create the "STSL-Settings" directory if it doesn't exist
if not exist "STSL-Settings" (
    mkdir "STSL-Settings"
)

REM Create the "Logs" directory if it doesn't exist
if not exist "Logs" (
    mkdir "Logs"
)

:: Check if the "flags.json" file exists
if exist "STSL-Settings\flags.json" (
    for /F "usebackq delims=" %%A in (`powershell -Command "Add-Type -AssemblyName System.Web.Extensions; $json = Get-Content -Path 'STSL-Settings\flags.json' -Raw; $obj = New-Object -TypeName System.Web.Script.Serialization.JavaScriptSerializer; $obj.DeserializeObject($json).userAgreement"`) do set "previousAnswer=%%A"
) else (
    set "previousAnswer=N"
)

set "originalAnswer=!previousAnswer!"
set "previousAnswer=!previousAnswer:~0,1!"
::echo Prev: !previousAnswer!
::echo Orig: !originalAnswer!

REM If the user had previously answered "Y" or "y," skip the prompt
if /i "!previousAnswer!"=="Y" (
    echo User has already agreed to the user agreement...
    goto startup
)

REM Display user agreement and prompt for input
echo Listen up buck-a-roo, this installer is going to install:
echo Chocolatey, GIT, Python10 (and a bunch of necessary Python add-ons), NVM, and Node.js, 
echo if they aren't on your system already.
echo We offer no warranty or guarantee on these installs. 
echo By pressing Y, you agree to these terms and the individual licenses of all the packages.

:input
set /p userInput=Do you want to continue? (Y/N): 

REM Convert user input to uppercase for comparison and JSON storage
set "userInput=!userInput:~0,1!"
for /f "tokens=* delims= " %%i in ("!userInput!") do set userInput=%%i

REM Check if the user input is valid (Y, y, N, or n)
if /i not "!userInput!"=="Y" if /i not "!userInput!"=="N" (
    echo Invalid input. Please enter Y or N.
    goto input
)

REM Save the user's answer to the "flags.json" file (always in uppercase)
(
    echo { "userAgreement": "!userInput!" }
) > "STSL-Settings\flags.json"

REM Check if the user wants to continue
if /i "!userInput!" NEQ "Y" (
    echo Exiting...
    exit /b 1
)

:installation
REM Continue with the installation steps...

:: Install Chocolatey
choco -v >nul 2>>"Logs\Gui-Launch-Errors.log"
if %errorlevel% equ 0 (
    echo Chocolatey is already installed. >>"Logs\Gui-Launch-Errors.log"
) else (
    echo Installing Chocolatey...
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
    if %errorlevel% neq 0 (
        echo Error installing Chocolatey. >>"Logs\Gui-Launch-Errors.log"
    ) else (
        echo Chocolatey installed successfully. >>"Logs\Gui-Launch-Errors.log"
    )
)

:: Install Git
git --version >nul 2>>"Logs\Gui-Launch-Errors.log"
if %errorlevel% equ 0 (
    echo Git is already installed. >>"Logs\Gui-Launch-Errors.log"
) else (
    echo Installing Git...
    choco install git -y
    if %errorlevel% neq 0 (
        echo Error installing Git. >>"Logs\Gui-Launch-Errors.log"
    ) else (
        echo Git installed successfully. >>"Logs\Gui-Launch-Errors.log"
    )
)

:: Install NVM
nvm version >nul 2>>"Logs\Gui-Launch-Errors.log"
if %errorlevel% equ 0 (
    echo NVM is already installed. >>"Logs\Gui-Launch-Errors.log"
) else (
    echo Installing NVM...
    choco install nvm -y
    if %errorlevel% neq 0 (
        echo Error installing NVM. >>"Logs\Gui-Launch-Errors.log"
    ) else (
        echo NVM installed successfully. >>"Logs\Gui-Launch-Errors.log"
    )
)

:: Install Python from the embedded folder
set "PythonDir=%~dp0python"
if exist "%PythonDir%" (
    echo Python is found in the embedded folder.
) else (
    echo Python is not found in the embedded folder. Exiting...
    exit /b 1
)

echo Adding Python to the PATH...
set "PATH=%PythonDir%;%PATH%"
set "PATH=%PythonDir%\Scripts;%PATH%"

:: Install pip for the embedded Python installation
echo Installing pip...
python "%PythonDir%\get-pip.py"
if %errorlevel% neq 0 (
    echo Error installing pip. >>"Logs\Gui-Launch-Errors.log"
) else (
    echo pip installed successfully. >>"Logs\Gui-Launch-Errors.log"
)

:: Install venv using pip
echo Installing venv...
python -m pip install venv

:: Create and activate a virtual environment
echo Creating and activating a virtual environment...
python -m venv venv
venv\Scripts\activate.bat

:: Install additional packages
pip install Pillow pywin32 summa

goto startup
REM Launch the "STLauncherGui.py" GUI
::start "" python STLauncherGui.py
:startup

::start cmd /k "%~dp0GUI-Dependencies.bat" & exit

REM Close the command window after a successful install or check
echo Please check that all dependencies installed correctly without errors
echo If you get errors, please close and run the "STSL GUI Launcher.bat" file again.
echo You may have to run "STSL GUI Launcher.bat" twice if you did not already have Python installed on your system for it to activate.
pause
::exit
