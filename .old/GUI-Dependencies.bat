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

REM Create the "Logs" directory if it doesn't exist
if not exist "Logs" (
    mkdir "Logs"
)

:: Activate the Pipenv environment
pipenv shell

:: Define the required software and corresponding error messages
set "software[0]=Chocolatey"
set "software[1]=GitPython"
set "software[2]=NVM"
set "software[3]=Python 3.10"
set "software[4]=Pillow"
set "software[5]=Tkinter"
set "software[6]=pywin32"

set "error[0]=Chocolatey is not installed. Run the "RUN FIRST Install GUI Dependencies.bat" file."
set "error[1]=GitPython is not installed. Run the "RUN FIRST Install GUI Dependencies.bat" file."
set "error[2]=NVM is not installed. Run the "RUN FIRST Install GUI Dependencies.bat" file."
set "error[3]=Python 3.10 is not found. Installing Python 3.10 using Chocolatey..."
set "error[4]=Pillow is not installed. Run the "RUN FIRST Install GUI Dependencies.bat" file."
set "error[5]=Tkinter is not installed. Run the "RUN FIRST Install GUI Dependencies.bat" file."
set "error[6]=pywin32 is not installed. Run the "RUN FIRST Install GUI Dependencies.bat" file."

:: Loop through the software array
for /L %%i in (0,1,6) do (
    :: Check if the software is already installed
    pip show %software[%%i]% >nul 2>&1
    if %errorlevel% equ 0 (
        echo %software[%%i]% is already installed.
    ) else (
        echo %error[%%i]%
        echo Please press any key to continue...
        pause >nul
        exit /b 1
    )
)

:StartGui
REM Launch the "STLauncherGui.py" GUI
python "%ParentFolder%\STLauncherGui.py"

REM Close the command window after a successful install or check
exit
