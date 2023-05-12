@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Define the path to the SillyTavern directory
set SillyTavernPath=%USERPROFILE%\Documents\SillyTavern

:: Check if SillyTavern is already installed
if exist "%SillyTavernPath%" (
    echo SillyTavern is already installed, skipping installation.
) else (
    echo Cloning SillyTavern...
    git clone https://github.com/Cohee1207/SillyTavern -b main "%SillyTavernPath%"
)

:: Go to the SillyTavern directory and run Start.bat in a new window
cd /d "%SillyTavernPath%"
echo Running Start.bat...
start cmd /k "Start.bat"

echo Process completed successfully.
pause >nul
