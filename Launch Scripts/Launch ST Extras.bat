@echo off
setlocal

REM Get the current script directory
set "scriptDir=%~dp0"

REM Extract the launcher version from the script directory
for %%I in ("%scriptDir%\..") do set "launcherVersion=%%~nxI"

REM Construct the path to the Install Scripts directory
set "installScriptsDir=%scriptDir%\..\Install Scripts"

REM Check if SillyTavernExtras is installed
if exist "%scriptDir%\..\..\SillyTavern-extras" (
    echo SillyTavernExtras is already installed.
    echo Launching SillyTavernExtras...
    start "" /b "%installScriptsDir%\3 - Install SillyTavernExtras - Optional.bat"
) else (
    echo SillyTavernExtras is not installed. Run "3 - Install SillyTavernExtras" from the GUI. 
    echo Exiting...
)

pause

endlocal
