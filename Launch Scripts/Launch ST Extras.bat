@echo off
setlocal

REM Check if SillyTavernExtras is installed
if exist "%~dp0..\..\SillyTavern-extras" (
    echo SillyTavernExtras is already installed.
    echo Launching SillyTavernExtras...
    start "" /b "%~dp0..\..\SillyTavernSimpleLauncher\Install Scripts\4 - Install SillyTavernExtras - Optional.bat"
) else (
    echo SillyTavernExtras is not installed. Run "4 - Install SillyTavernExtras" from the GUI. 
    echo Exiting...
)

pause

endlocal
