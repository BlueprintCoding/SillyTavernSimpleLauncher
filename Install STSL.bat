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

REM Check if winget is installed
winget --version >nul 2>&1

REM If winget is not installed, install it
if errorlevel 1 (
    echo winget is not installed. Installing winget...
    @powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://aka.ms/installwinget'))"
)

REM Check if Python is installed
set "python_exe="
for /f "delims=" %%i in ('python -c "import sys; print(sys.executable)"') do (
    set "python_exe=%%i"
)
if not defined python_exe (
 echo Python is not installed. Installing Python 3.10...
     winget install -e --id Python.Python.3.10
)

REM Check if pip is installed
pip --version >nul 2>&1

REM If pip is not installed, install it
if errorlevel 1 (
    echo pip is not installed. Installing pip...
    python -m ensurepip --upgrade
)



REM Check if Git is installed
git --version >nul 2>&1

REM If Git is not installed, install it using winget
if errorlevel 1 (
    echo Git is not installed. Installing Git...
     winget install --id Git.Git -e --source winget
)

REM Check if Node.js LTS is installed
node --version >nul 2>&1

REM If Node.js LTS is not installed, install it using winget
if errorlevel 1 (
    echo Node.js LTS is not installed. Installing Node.js LTS...
    winget install -e --id OpenJS.NodeJS.LTS
)


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
python -m pip install flask nltk transformers requests tqdm

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
