@echo off
setlocal enabledelayedexpansion

REM Set the script and config file paths
set "script_path=%~dp0"
set "main_branch_config_file=%script_path%..\..\SillyTavern-MainBranch\config.conf"
set "dev_branch_config_file=%script_path%..\..\SillyTavern-DevBranch\config.conf"

REM Prompt the user to choose the branch
echo Select the branch:
echo 1) Main Branch
echo 2) Dev Branch
set /p "branch=Enter the branch number (1 or 2): "

REM Set the config file path based on the branch selection
if "%branch%"=="1" (
    set "config_file=%main_branch_config_file%"
) else if "%branch%"=="2" (
    set "config_file=%dev_branch_config_file%"
) else (
    echo Invalid branch selection. Exiting...
    exit /b 1
)

REM Read the existing default values from the config file
for /f "usebackq tokens=1,* delims== " %%a in ("%config_file%") do (
    if "%%a"=="const" (
        set "option=%%b"
    ) else if defined option (
        setlocal enabledelayedexpansion
        for %%i in ("!option!") do (
            set "%%a=%%~i"
        )
        endlocal
        set "option="
    )
)

echo Existing default values:
echo port: %port%
echo whitelist: %whitelist%
echo whitelistMode: %whitelistMode%
echo basicAuthMode: %basicAuthMode%
echo basicAuthUser: %basicAuthUser%
echo disableThumbnails: %disableThumbnails%
echo autorun: %autorun%
echo enableExtensions: %enableExtensions%
echo listen: %listen%
echo allowKeysExposure: %allowKeysExposure%
echo.

REM Prompt the user for new values
set /p "port=Enter new port: "
set /p "whitelist=Enter new whitelist (separate multiple IPs with a space): "
set /p "whitelistMode=Enter new whitelist mode (true/false): "
set /p "basicAuthMode=Enter new basic authentication mode (true/false): "
set /p "basicAuthUser=Enter new basic authentication user (in the format username:password): "
set /p "disableThumbnails=Enter new disable thumbnails mode (true/false): "
set /p "autorun=Enter new autorun mode (true/false): "
set /p "enableExtensions=Enter new enable extensions mode (true/false): "
set /p "listen=Enter new listen mode (true/false): "
set /p "allowKeysExposure=Enter new allow keys exposure mode (true/false): "

REM Update the config file with the new values
echo.
echo Updating config file...
echo.
(
    echo const port = %port%; 
    echo const whitelist = [%whitelist%]; 
    echo const whitelistMode = %whitelistMode%; 
    echo const basicAuthMode = %basicAuthMode%; 
    echo const basicAuthUser = {username: "%basicAuthUser:~0,-1%", password: "%basicAuthUser:~-%}; 
    echo const disableThumbnails = %disableThumbnails%; 
    echo const autorun = %autorun%; 
    echo const enableExtensions = %enableExtensions%; 
    echo const listen = %listen%; 
    echo const allowKeysExposure = %allowKeysExposure%; 
    echo.
    echo module.exports = {
    echo   port,
    echo   whitelist,
    echo   whitelistMode,
    echo   basicAuthMode,
    echo   basicAuthUser,
    echo   disableThumbnails,
    echo   autorun,
    echo   enableExtensions,
    echo   listen,
    echo   allowKeysExposure,
    echo };
) > "%config_file%"

echo Config file updated successfully.

endlocal

