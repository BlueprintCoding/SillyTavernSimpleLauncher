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

:: Define the required software and corresponding error messages
set "software[0]=Chocolatey"
set "software[1]=Git"
set "software[2]=NVM"
set "software[3]=Python 3.10"
set "software[4]=Pillow"
set "software[5]=Tkinter"
set "software[6]=pywin32"

set "error[0]=Chocolatey is not installed, run the "RUN FIRST Install GUI Dependencies.bat"."
set "error[1]=Git is not installed, run the "RUN FIRST Install GUI Dependencies.bat"."
set "error[2]=NVM is not installed, run the "RUN FIRST Install GUI Dependencies.bat"."
set "error[3]=Python 3.10 is not found. Installing Python 3.10 using Chocolatey..."
set "error[4]=Pillow is not installed, run the "RUN FIRST Install GUI Dependencies.bat"."
set "error[5]=Tkinter is not installed, run the "RUN FIRST Install GUI Dependencies.bat"."
set "error[6]=pywin32 is not installed, run the "RUN FIRST Install GUI Dependencies.bat"."

:: Loop through the software array
for /L %%i in (0,1,6) do (
    :: Check if the software is already installed
    python -c "import %software[%%i]%" >nul 2>&1
    if %errorlevel% equ 0 (
        echo %software[%%i]% is already installed.
    ) else (
        echo %error[%%i]%
        start cmd /k "%~dp0STSL GUI Launcher.bat" & exit
    )
)
call venv\Scripts\activate.bat
REM Launch the "STLauncherGui.py" GUI
start "" python STLauncherGui.py

REM Close the command window after a successful install or check
exit
