@echo off

REM Check if Python 3.10 or higher is installed
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore\3.10" >NUL 2>NUL
if errorlevel 1 (
    echo Python 3.10 or higher is not installed. Installing Python 3.10...
    REM Download and install Python 3.10
    REM Replace the URL below with the appropriate download link for your system
    REM Make sure to update the installation path as well, if needed
    curl -o python310.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    start /wait python310.exe /quiet InstallAllUsers=1 PrependPath=1 Include_launcher=0
    del python310.exe
) else (
    echo Python 3.10 or higher is already installed.
)

REM Check if Tkinter is installed
python -c "import tkinter" 2>NUL

REM If Tkinter is not installed, install it
if errorlevel 1 (
    echo Tkinter is not installed. Installing Tkinter...
    REM Install Tkinter using pip
    python -m pip install tkinter
) else (
    echo Tkinter is already installed.
)

REM Launch the "STLauncherGui.py" GUI
start "" python STLauncherGui.py

REM Close the command window after a successful install or check
exit
