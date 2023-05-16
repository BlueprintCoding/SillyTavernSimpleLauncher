@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Get the path of the parent folder
for %%I in ("%~dp0..\..") do set "ParentFolder=%%~fI"

:: Define the path to the SillyTavern directory
set "SillyTavernPath=%ParentFolder%\SillyTavern-DevBranch"

:: Check if SillyTavern is already installed
if exist "%SillyTavernPath%" (
    echo SillyTavern is already installed, skipping installation.
) else (
    echo Cloning SillyTavern...
    git clone https://github.com/Cohee1207/SillyTavern -b dev "%SillyTavernPath%"
)
:: Go to the SillyTavern directory and run Start.bat in a new window
::cd /d "%SillyTavernPath%"
::echo Running Start.bat...
::start cmd /k "Start.bat"

echo SillyTavern Dev Branch Cloned Successfully.
pause >nul