@echo off
setlocal

REM Check if SillyTavernExtras is installed
if exist "%~dp0..\..\SillyTavern-extras" (
    echo SillyTavernExtras is already installed.
    echo Launching SillyTavernExtras...
    start "" /b "%~dp0..\..\SillyTavern-extras\Start.bat"
) else (
    echo SillyTavernExtras is not installed. Run "4 - Install SillyTavernExtras" from the GUI. 
    echo Exiting...
)

pause

endlocal
