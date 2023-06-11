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
REM Set the root directory to the directory containing this batch file
set "root_dir=%~dp0"

REM Check if Python is installed
set "python_exe="
for /f "delims=" %%i in ('python -c "import sys; print(sys.executable)"') do (
    set "python_exe=%%i"
)
if not defined python_exe (
    echo Python is not installed.
    echo Please install Python by visiting the Python installer website. Please install version 3.10 for maximum compatibility.
    echo Please install Python as admin and make sure it is added to the system PATH. Install pip if it gives you the option.
    start "" "https://www.python.org/downloads/release/python-31011/"
    pause
    exit /b
)

REM Check if pip is installed
pip --version >nul 2>&1

REM If pip is not installed, install it
if errorlevel 1 (
    echo pip is not installed. Installing pip...
    python -m ensurepip --upgrade
)

REM Check if Chocolatey is installed
choco --version >nul 2>&1

REM If Chocolatey is not installed, install it
if errorlevel 1 (
    echo Chocolatey is not installed. Installing Chocolatey...
    @powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
)

REM Install Node.js LTS via Chocolatey
echo Installing Node.js LTS...
choco install nodejs-lts --force -y

REM Check if venv exists
if not exist venv (
    echo Creating a new virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Install required Python packages
echo Installing required Python packages...
python -m pip install --upgrade pip
python -m pip install flask nltk transformers

REM Download NLTK resources
echo Downloading NLTK resources...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')"


echo All requirements installed successfully.

REM Launch the app.py server
cd "%root_dir%"
echo Launching the server...
start /b python app.py

REM Wait for the server to start
:wait
timeout /t 1 >nul
tasklist /fi "imagename eq python.exe" | find /i "python.exe" >nul 2>&1
if errorlevel 1 goto wait

REM Open the browser to localhost:6969
echo Opening the browser...
start "" "http://localhost:6969"

pause
