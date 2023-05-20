@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Get the path of the parent folder
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


REM Check if the user-agreement file exists
if exist user-agreement.txt (
    for /F "tokens=*" %%A in (user-agreement.txt) do set previousAnswer=%%A
) else (
    set previousAnswer=N
)


set previousAnswer=%previousAnswer:~0,1%

REM If the user had previously answered "Y," skip the prompt
if /i "%previousAnswer%"=="Y" (
    echo User has already agreed to user agreement...
    goto installation
)

REM Display user agreement and prompt for input
echo Listen up buck-a-roo, this installer is going to install:
echo Chocolatey, GIT, Python10 (and a bunch of necessary Python add-ons), NVM, and Node.js, 
echo if they aren't on your system already.
echo We offer no warranty or guarantee on these installs. 
echo By pressing Y, you agree to these terms and the individual licenses of all the packages.

:input
set /p userInput=Do you want to continue? (Y/N): 

REM Convert user input to uppercase for comparison
set userInput=%userInput:~0,1%

REM Check if the user input is valid (Y, y, N, or n)
if /i not "%userInput%"=="Y" if /i not "%userInput%"=="N" (
    echo Invalid input. Please enter Y or N.
    goto input
)

REM Save the user's answer to the user-agreement file (always in uppercase)
echo %userInput% > user-agreement.txt

REM Check if the user wants to continue
if /i "%userInput%" NEQ "Y" (
    echo Exiting...
    exit /b 1
)

:installation
REM Continue with the installation steps...


:: Check if Chocolatey is already installed
choco -v >nul 2>&1
if %errorlevel% equ 0 (
    echo Chocolatey is already installed.
) else (
    echo Installing Chocolatey...
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

)

:: Check if Git is already installed
git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Git is already installed.
) else (
    echo Installing Git...
    choco install git -y
)

:: Check if NVM is already installed
nvm version >nul 2>&1
if %errorlevel% equ 0 (
    echo NVM is already installed.
) else (
    echo Installing NVM...
    choco install nvm -y
)

REM Check if Python 3.10 is installed
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python is not found via the system path. Checking alternative locations...

    :: Check if Python 3.10 is installed in Program Files directory
    if exist "C:\Program Files\Python310" (
        echo Python 3.10 is installed in C:\Program Files\Python310.
        set "PythonDir=C:\Program Files\Python310"
    ) else (
        :: Check if Python 3.10 is installed in user-specific directory
        set "PythonDir=C:\Users%username%\AppData\Local\Programs\Python\Python310"
        if exist "%PythonDir%" (
            echo Python 3.10 is installed in %PythonDir%.
        ) else (
            echo Python 3.10 is not found in the specified locations. Installing Python 3.10 using Chocolatey...
            REM Install Python 3.10 using Chocolatey
            choco install python310 -y --force
            set "PythonDir=C:\Program Files\Python310"
        )
    )

) else (
    echo Python 3.10 is already found via the system path.
set "PythonDir="
)

if not "%PythonDir%"=="" (
echo Adding Python to the PATH...
setx PATH "%PythonDir%;%PATH%"
)

:: Check if Pillow is already installed
python -c "import PIL" >nul 2>&1
if %errorlevel% equ 0 (
echo Pillow is already installed.
) else (
echo Installing Pillow...
python -m pip install pillow
)

:: Check if Tkinter is already installed
python -c "import tkinter" >nul 2>&1
if %errorlevel% equ 0 (
echo Tkinter is already installed.
) else (
echo Installing Tkinter...
python -m pip install tkinter
)

:: Check if pywin32 is installed
python -c "import win32api" >nul 2>&1
if %errorlevel% equ 0 (
echo pywin32 is already installed.
) else (
echo Installing pywin32...
python -m pip install pywin32
)

REM Launch the "STLauncherGui.py" GUI
::start "" python STLauncherGui.py


start cmd /k "%~dp0GUI-Dependencies.bat" & exit

REM Close the command window after a successful install or check
echo Please check that all dependencies installed correctly without errors
echo If you get errors, please close and run the "STSL GUI Launcher.bat" file again.
pause
exit