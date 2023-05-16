@echo off
setlocal

set branchName=SillyTavern-MainBranch

REM Check if the directories for main exist
if not exist "%~dp0..\..\%branchName%\" (
    echo The directory for %branchName% does not exist... Run "3a - Install SillyTavern - Main Branch" from the GUI. 
) else (
REM Launch the Start.bat file in the chosen branch in a new window
echo Launching Silly Tavern Main Branch
start "" /b "%~dp0..\..\%branchName%\Start.bat"
)

pause

endlocal
