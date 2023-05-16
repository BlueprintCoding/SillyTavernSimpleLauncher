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

:: Get the path of the parent folder
for %%I in ("%~dp0..\..\..") do set "ParentFolder=%%~fI"


REM Create the ST-Backups folder if it doesn't exist
set "backup_folder=%ParentFolder%\SillyTavern-FileBackups"
if not exist "%ParentFolder%" mkdir "%backup_folder%"

REM Create a dated directory with timestamp for the copied files
set "timestamp=%time:~0,2%%time:~3,2%%time:~6,2%"  REM Format: HHMMSS
set "datestamp=%date:~10,4%%date:~4,2%%date:~7,2%"  REM Format: YYYYMMDD

REM Backup from SillyTavern-MainBranch
set "main_branch=%ParentFolder%\SillyTavern-MainBranch"
set "main_destination_folder=%backup_folder%\MainBranch\%datestamp%_%timestamp%"
mkdir "%main_destination_folder%"
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\Backgrounds" "%main_destination_folder%\Backgrounds" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\Characters" "%main_destination_folder%\Characters" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\Chats" "%main_destination_folder%\Chats" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\Groups" "%main_destination_folder%\Groups" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\Group chats" "%main_destination_folder%\Group chats" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\KoboldAI Settings" "%main_destination_folder%\KoboldAI Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\NovelAI Settings" "%main_destination_folder%\NovelAI Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\OpenAI Settings" "%main_destination_folder%\OpenAI Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\TextGen Settings" "%main_destination_folder%\TextGen Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\Themes" "%main_destination_folder%\Themes" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\User Avatars" "%main_destination_folder%\User Avatars" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%main_branch%\public\Worlds" "%main_destination_folder%\Worlds" /E
copy "%main_branch%\public\settings.json" "%main_destination_folder%"

REM Backup from SillyTavern-DevBranch
set "dev_branch=%ParentFolder%\SillyTavern-DevBranch"
set "dev_destination_folder=%backup_folder%\DevBranch\%datestamp%_%timestamp%"
mkdir "%dev_destination_folder%"
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\Backgrounds" "%dev_destination_folder%\Backgrounds" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\Characters" "%dev_destination_folder%\Characters" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\Chats" "%dev_destination_folder%\Chats" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\Groups" "%dev_destination_folder%\Groups" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\Group chats" "%dev_destination_folder%\Group chats" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\KoboldAI Settings" "%dev_destination_folder%\KoboldAI Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\NovelAI Settings" "%dev_destination_folder%\NovelAI Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\OpenAI Settings" "%dev_destination_folder%\OpenAI Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\TextGen Settings" "%dev_destination_folder%\TextGen Settings" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\Themes" "%dev_destination_folder%\Themes" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\User Avatars" "%dev_destination_folder%\User Avatars" /E
"%SYSTEMROOT%\System32\robocopy.exe" "%dev_branch%\public\Worlds" "%dev_destination_folder%\Worlds" /E
copy "%dev_branch%\public\settings.json" "%dev_destination_folder%"

echo Backup completed successfully.
pause

