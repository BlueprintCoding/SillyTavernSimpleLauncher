@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
setlocal

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
:: Set the root directory to the directory containing this batch file
set "root_dir=%~dp0"

:: Set the temporary directory for installers
set "temp_dir=installer_temp"

:: Create the temporary directory
if not exist "%temp_dir%" mkdir "%temp_dir%"

:: Check if Python is installed
where python >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Downloading Python 3.10...
    :: Set the installer file name
    set "python_installer=%temp_dir%\python_installer.exe"
    :: Enable delayed expansion for this variable
    setlocal enabledelayedexpansion
    :: Download the Python 3.10 installer
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile !python_installer!"
    :: Indicate start of installation
    echo Starting Python installation. This might take a few minutes...
    :: Install Python in silent mode
    start /wait "" "!python_installer!" /quiet InstallAllUsers=1 TargetDir=%SystemDrive%\Python310 PrependPath=1 Include_test=0
    :: Indicate end of installation
    echo Python installation completed.
    :: Return to normal expansion
    endlocal
)

:: Check if pip is installed
where pip >nul 2>&1
if errorlevel 1 (
    echo pip is not installed. Installing pip...
    :: Set the get-pip script file path
    set "get_pip_script=%~dp0get-pip.py"
    :: Install pip using the get-pip script
    python "%get_pip_script%"
    echo pip has been successfully installed.
)



:: Check if Git is installed
where git >nul 2>&1
if errorlevel 1 (
    echo Git is not detected on your system. Starting installation process...
    :: Set the installer file name
    set "git_installer=%temp_dir%\git_installer.exe"
    :: Enable delayed expansion for this variable
    setlocal enabledelayedexpansion
    echo Downloading Git. Please wait, this may take a few minutes depending on your network speed...
    :: Download the Git installer
    powershell -Command "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.33.1.windows.1/Git-2.33.1-64-bit.exe -OutFile !git_installer!"
    echo Starting the installation of Git. This might take a few minutes...
    :: Install Git in silent mode
    "!git_installer!" /VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /NOICONS /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"
    echo Git has been successfully installed.
    :: Return to normal expansion
    endlocal
)


:: Check if Node.js LTS is installed
where node >nul 2>&1
if errorlevel 1 (
    echo Node.js LTS is not detected on your system. Starting installation process...
    :: Set the installer file name
    set "node_installer=%temp_dir%\node-lts.msi"
    :: Enable delayed expansion for this variable
    setlocal enabledelayedexpansion
    echo Downloading Node.js LTS. Please wait, this may take a few minutes depending on your network speed...
    :: Download the specific Node.js LTS version
    powershell -Command "Invoke-WebRequest -Uri https://nodejs.org/dist/v18.16.1/node-v18.16.1-x64.msi -OutFile !node_installer!"
    echo Starting the installation of Node.js LTS. This might take a few minutes...
    :: Install Node.js in silent mode
    msiexec /i "!node_installer!" /qn
    echo Node.js LTS has been successfully installed.
    :: Return to normal expansion
    endlocal
)



:: Delete the temporary directory
rd /s /q "%temp_dir%"

REM Check if venv exists
if not exist venv (
    echo Creating a new virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate.bat


echo Installing required Python packages, this could take a few minutes...
python -m pip install flask nltk transformers requests tqdm

REM Download NLTK resources
echo Downloading NLTK resources...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')"
echo Python packagesnode installed...

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
endlocal
