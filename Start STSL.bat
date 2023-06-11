@echo off

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
if errorlevel 1 (
    echo pip is not installed.
    echo Please run "Install STSL.bat" to install all the requirements.
    pause
    exit /b
)

REM Check if NVM is installed
nvm version >nul 2>&1
if errorlevel 1 (
    echo NVM is not installed.
    echo Please run "Install STSL.bat" to install all the requirements.
    pause
    exit /b
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed.
    echo Please run "Install STSL.bat" to install all the requirements.
    pause
    exit /b
)

REM Check if the virtual environment exists
if not exist "%root_dir%\venv" (
    echo Virtual environment not found.
    echo Please run "Install STSL.bat" to install all the requirements.
    pause
    exit /b
)
REM Activate the virtual environment
call "%root_dir%\venv\Scripts\activate.bat"

REM Check if required Python packages are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Required Python packages are not installed.
    echo Please run "Install STSL.bat" to install all the requirements.
    pause
    exit /b
)

REM Check if NLTK resources are downloaded
python -c "import nltk; nltk.data.find('tokenizers/punkt')" >nul 2>&1
if errorlevel 1 (
    echo NLTK resources are not downloaded.
    echo Please run "Install STSL.bat" to install all the requirements.
    pause
    exit /b
)

REM All requirements are installed
echo All requirements are already installed. Launching the server...

REM Launch the app.py server
cd "%root_dir%"
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
