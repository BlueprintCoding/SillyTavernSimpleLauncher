@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

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

:: Create and activate a virtual environment
python -m venv venv
call venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip

:: Install Chocolatey
choco -v >nul 2>>"GUI-Launch-Errors.txt"
if %errorlevel% equ 0 (
    echo Chocolatey is already installed. >>"GUI-Launch-Errors.txt"
) else (
    echo Installing Chocolatey...
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
    if %errorlevel% neq 0 (
        echo Error installing Chocolatey. >>"GUI-Launch-Errors.txt"
    ) else (
        echo Chocolatey installed successfully. >>"GUI-Launch-Errors.txt"
    )
)

:: Install Git
git --version >nul 2>>"GUI-Launch-Errors.txt"
if %errorlevel% equ 0 (
    echo Git is already installed. >>"GUI-Launch-Errors.txt"
) else (
    echo Installing Git...
    choco install git -y
    if %errorlevel% neq 0 (
        echo Error installing Git. >>"GUI-Launch-Errors.txt"
    ) else (
        echo Git installed successfully. >>"GUI-Launch-Errors.txt"
    )
)

:: Install NVM
nvm version >nul 2>>"GUI-Launch-Errors.txt"
if %errorlevel% equ 0 (
    echo NVM is already installed. >>"GUI-Launch-Errors.txt"
) else (
    echo Installing NVM...
    choco install nvm -y
    if %errorlevel% neq 0 (
        echo Error installing NVM. >>"GUI-Launch-Errors.txt"
    ) else (
        echo NVM installed successfully. >>"GUI-Launch-Errors.txt"
    )
)

:: Install Python 3.10
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
            if %errorlevel% neq 0 (
                echo Error installing Python 3.10. >>"GUI-Launch-Errors.txt"
            ) else (
                echo Python 3.10 installed successfully. >>"GUI-Launch-Errors.txt"
                set "PythonDir=C:\Program Files\Python310"
            )
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

:: Install Pillow
python -c "import PIL" >nul 2>>"GUI-Launch-Errors.txt"
if %errorlevel% equ 0 (
    echo Pillow is already installed. >>"GUI-Launch-Errors.txt"
) else (
    echo Installing Pillow...
    python -m pip install --upgrade pillow
    if %errorlevel% neq 0 (
        echo Error installing Pillow. >>"GUI-Launch-Errors.txt"
    ) else (
        echo Pillow installed successfully. >>"GUI-Launch-Errors.txt"
    )
)

:: Install Tkinter
python -c "import tkinter" >nul 2>>"GUI-Launch-Errors.txt"
if %errorlevel% equ 0 (
    echo Tkinter is already installed. >>"GUI-Launch-Errors.txt"
) else (
    echo Installing Tkinter...
    python -m pip install --upgrade tkinter
    if %errorlevel% neq 0 (
        echo Error installing Tkinter. >>"GUI-Launch-Errors.txt"
    ) else (
        echo Tkinter installed successfully. >>"GUI-Launch-Errors.txt"
    )
)

:: Install pywin32
python -c "import win32api" >nul 2>>"GUI-Launch-Errors.txt"
if %errorlevel% equ 0 (
    echo pywin32 is already installed. >>"GUI-Launch-Errors.txt"
) else (
    echo Installing pywin32...
    python -m pip install --upgrade pywin32
    if %errorlevel% neq 0 (
        echo Error installing pywin32. >>"GUI-Launch-Errors.txt"
    ) else (
        echo pywin32 installed successfully. >>"GUI-Launch-Errors.txt"
    )
)

REM Launch the "STLauncherGui.py" GUI
::start "" python STLauncherGui.py

start cmd /k "%~dp0GUI-Dependencies.bat" & exit

REM Close the command window after a successful install or check
echo Please check that all dependencies installed correctly without errors
echo If you get errors, please close and run the "STSL GUI Launcher.bat" file again.
echo You may have to run "STSL GUI Launcher.bat" twice if you did not already have Python installed on your system for it to activate.
pause
::exit
