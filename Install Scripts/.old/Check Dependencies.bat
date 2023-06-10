@echo off

set LOG_FILE=dependencies-log.txt

echo Checking dependencies...

REM Check if Chocolatey is installed
choco --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Chocolatey is not installed. Run "STSL GUI Launcher.bat" to install.
    echo [%date% %time%] Chocolatey is not installed. Run "STSL GUI Launcher.bat" to install. >> %LOG_FILE%
) else (
    echo Chocolatey is installed.
    echo [%date% %time%] Chocolatey is installed. >> %LOG_FILE%
)

REM Check if Git is installed
git --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Run "STSL GUI Launcher.bat" to install.
    echo [%date% %time%] Git is not installed. Run "STSL GUI Launcher.bat" to install. >> %LOG_FILE%
) else (
    echo Git is installed.
    echo [%date% %time%] Git is installed. >> %LOG_FILE%
)

REM Load NVM environment
echo Loading NVM environment...
CALL "%SystemDrive%\ProgramData\nvm\nvm.exe" > nul

REM Check if NVM is installed
nvm version > nul 2>&1
if %errorlevel% neq 0 (
    echo NVM is not installed. Run "STSL GUI Launcher.bat" to install.
    echo [%date% %time%] NVM is not installed. Run "STSL GUI Launcher.bat" to install. >> %LOG_FILE%
) else (
    echo NVM is installed.
    echo [%date% %time%] NVM is installed. >> %LOG_FILE%
)

REM Check if Node.js 18 is installed
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js 18 is not installed. Run "Install SillyTavern Dependencies" to install.
    echo [%date% %time%] Node.js 18 is not installed. Run "Install SillyTavern Dependencies" to install. >> %LOG_FILE%
) else (
    echo Node.js 18 is installed.
    echo [%date% %time%] Node.js 18 is installed. >> %LOG_FILE%
)

REM Check if Python 18 is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python 18 is not installed. Run "STSL GUI Launcher.bat" to install.
    echo [%date% %time%] Python 10 is not installed or activated. Close the GUI and Run "STSL GUI Launcher.bat" to install/activate. >> %LOG_FILE%
) else (
    echo Python 18 is installed.
    echo [%date% %time%] Python 10 is installed. >> %LOG_FILE%
)

REM Check if Tkinter is installed
python -c "import tkinter" > nul 2>&1
if %errorlevel% neq 0 (
    echo Tkinter is not installed. Run "STSL GUI Launcher.bat" to install.
    echo [%date% %time%] Tkinter is not installed. Run "STSL GUI Launcher.bat" to install. >> %LOG_FILE%
) else (
    echo Tkinter is installed.
    echo [%date% %time%] Tkinter is installed. >> %LOG_FILE%
)

REM Check if pyperclip is installed
python -c "import pyperclip" > nul 2>&1
if %errorlevel% neq 0 (
    echo pyperclip is not installed. Run "OptmizePrompt Gui" to install.
    echo [%date% %time%] pyperclip is not installed. Run "OptmizePrompt Gui" to install. >> %LOG_FILE%
) else (
    echo pyperclip is installed.
    echo [%date% %time%] pyperclip is installed. >> %LOG_FILE%
)

REM Check if nltk is installed
python -c "import nltk" > nul 2>&1
if %errorlevel% neq 0 (
    echo nltk is not installed. Run "OptmizePrompt Gui" to install.
    echo [%date% %time%] nltk is not installed. Run "OptmizePrompt Gui" to install. >> %LOG_FILE%
) else (
    echo nltk is installed.
    echo [%date% %time%] nltk is installed. >> %LOG_FILE%
)

REM Check if Pillow is installed
python -c "import PIL" > nul 2>&1
if %errorlevel% neq 0 (
    echo Pillow is not installed. Run "STSL GUI Launcher.bat" to install.
    echo [%date% %time%] Pillow is not installed. Run "STSL GUI Launcher.bat" to install. >> %LOG_FILE%
) else (
    echo Pillow is installed.
    echo [%date% %time%] Pillow is installed. >> %LOG_FILE%
)

echo Dependencies check complete.
echo [%date% %time%] Dependencies check complete. >> %LOG_FILE%
pause
