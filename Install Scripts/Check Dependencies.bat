@echo off

echo Checking dependencies...

REM Check if Chocolatey is installed
choco --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Chocolatey is not installed. Run "STSL GUI Launcher.bat" to install.
) else (
    echo Chocolatey is installed.
)

REM Check if Git is installed
git --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Run "STSL GUI Launcher.bat" to install.
) else (
    echo Git is installed.
)

REM Load NVM environment
echo Loading NVM environment...
CALL "%SystemDrive%\ProgramData\nvm\nvm.exe" > nul

REM Check if NVM is installed
nvm version > nul 2>&1
if %errorlevel% neq 0 (
    echo NVM is not installed. Run "STSL GUI Launcher.bat" to install.
) else (
    echo NVM is installed.
)

REM Check if Node.js 18 is installed
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js 18 is not installed. Run "Install SillyTavern Dependencies" to install.
) else (
    echo Node.js 18 is installed.
)

REM Check if Python 18 is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python 18 is not installed. Run "STSL GUI Launcher.bat" to install.
) else (
    echo Python 18 is installed.
)

REM Check if Tkinter is installed
python -c "import tkinter" > nul 2>&1
if %errorlevel% neq 0 (
    echo Tkinter is not installed. Run "STSL GUI Launcher.bat" to install.
) else (
    echo Tkinter is installed.
)

REM Check if pyperclip is installed
python -c "import pyperclip" > nul 2>&1
if %errorlevel% neq 0 (
    echo pyperclip is not installed. Run "OptmizePrompt Gui" to install.
) else (
    echo pyperclip is installed.
)

REM Check if nltk is installed
python -c "import nltk" > nul 2>&1
if %errorlevel% neq 0 (
    echo nltk is not installed. Run "OptmizePrompt Gui" to install.
) else (
    echo nltk is installed.
)

REM Check if Pillow is installed
python -c "import PIL" > nul 2>&1
if %errorlevel% neq 0 (
    echo Pillow is not installed. Run "STSL GUI Launcher.bat" to install.
) else (
    echo Pillow is installed.
)

echo Dependencies check complete.
pause
