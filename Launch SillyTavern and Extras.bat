@echo off
setlocal

REM Prompt the user to choose the branch to launch
echo Please choose the branch to launch:
echo 1. SillyTavern-MainBranch
echo 2. SillyTavern-DevBranch
set /p branch=Enter choice (1 or 2): 

REM Validate the user's choice
if "%branch%"=="1" (
    set branchName=SillyTavern-MainBranch
) else if "%branch%"=="2" (
    set branchName=SillyTavern-DevBranch
) else (
    echo Invalid choice. Exiting...
    exit /b
)

REM Check if the directories for main and dev exist
if not exist "%~dp0..\%branchName%\" (
    echo The directory for %branchName% does not exist... 
    echo Opening the "\SillyTavernSimpleLauncher\Install Scripts" so you can install...
	 REM Open the directory in File Explorer
    explorer "%~dp0..\SillyTavernSimpleLauncher\Install Scripts\"
    pause
    exit /b
)

REM Prompt the user to choose whether to launch SillyTavernExtras
echo Do you want to launch SillyTavernExtras?
echo 1. Yes ("Extras will be installed if it is not already")
echo 2. No
set /p launchExtras=Enter choice (1 or 2): 

REM Validate the user's choice
if "%launchExtras%"=="1" (
    set launchExtras=true
) else if "%launchExtras%"=="2" (
    set launchExtras=false
) else (
    echo Invalid choice. Exiting...
    exit /b
)

REM Launch the Start.bat file in the chosen branch in a new window
start "" /b "%~dp0..\%branchName%\Start.bat"

REM Check if SillyTavernExtras should be launched
if "%launchExtras%"=="true" (
    REM Define the path to the SillyTavernSimpleLauncher\Install Scripts directory
    set "installScriptsPath=%~dp0\Install Scripts"
    
    REM Launch the "4 - Install SillyTavernExtras - Optional.bat" file
    echo Installing SillyTavernExtras...
    start "" /b "%~dp0..\SillyTavernSimpleLauncher\Install Scripts\4 - Install SillyTavernExtras - Optional.bat"
)

endlocal
