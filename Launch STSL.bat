@echo off

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

REM Install NVM
echo Installing NVM...
python -m pip install nvm

REM Set up NVM environment variables
echo Setting up NVM environment variables...
call nvm setup

REM Install the latest LTS version of Node.js using NVM
echo Installing Node.js LTS...
call nvm install lts

REM Use the installed Node.js version
call nvm use lts

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
python -m nltk.downloader punkt stopwords averaged_perceptron_tagger maxent_ne_chunker words

echo All requirements installed successfully.

REM Launch the app.py server
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
