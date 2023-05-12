@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

REM Get the user's Documents folder path
set "documents_folder=%USERPROFILE%\Documents"

REM Create the ST-Backups folder if it doesn't exist
set "backup_folder=%documents_folder%\ST-Backups"
if not exist "%backup_folder%" mkdir "%backup_folder%"

REM Create a dated directory with timestamp for the copied files
set "timestamp=%time:~0,2%%time:~3,2%%time:~6,2%"  REM Format: HHMMSS
set "datestamp=%date:~10,4%%date:~4,2%%date:~7,2%"  REM Format: YYYYMMDD
set "destination_folder=%backup_folder%\%datestamp%_%timestamp%"
mkdir "%destination_folder%"

REM Copy the specified directories and files using robocopy
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\Backgrounds" "%destination_folder%\Backgrounds" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\Characters" "%destination_folder%\Characters" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\Chats" "%destination_folder%\Chats" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\Groups" "%destination_folder%\Groups" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\Group chats" "%destination_folder%\Group chats" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\KoboldAI Settings" "%destination_folder%\KoboldAI Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\NovelAI Settings" "%destination_folder%\NovelAI Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\OpenAI Settings" "%destination_folder%\OpenAI Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\TextGen Settings" "%destination_folder%\TextGen Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\Themes" "%destination_folder%\Themes" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\User Avatars" "%destination_folder%\User Avatars" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%documents_folder%\SillyTavern\public\Worlds" "%destination_folder%\Worlds" /E
copy "%documents_folder%\SillyTavern\public\settings.json" "%destination_folder%"


echo Backup completed successfully.
pause
