@echo off
setlocal

rem Check if running in a new/fresh console window
tasklist /FI "WINDOWTITLE eq %~nx0" 2>NUL | find /I "%~nx0" >NUL
if not errorlevel 1 (
    rem Running in the py.exe console, open in a new console window
    start "" "%~dp0%~nx0"
    exit
)

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
