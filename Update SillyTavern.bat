@echo off
set main_dir=%USERPROFILE%\Documents\SillyTavern
set dev_dir=%USERPROFILE%\Documents\SillyTavernDevBranch
set extras_dir=%USERPROFILE%\Documents\SillyTavern-extras

echo Updating SillyTavern instances:
echo.

:PromptUpdate
set /p update_main=Do you want to backup your Character, Chats, etc? (Y/N):
if /i "%update_main%"=="Y" (
    echo Backing up files... Please wait to confirm backup in "\Documents\ST-Backups"
    call  "%~dp0Backup SillyTavern Files.bat"
    echo.
)

:PromptUpdate
set /p update_main=Update main branch instance? (Y/N):
if /i "%update_main%"=="Y" (
    echo Updating main branch instance...
    cd /D "%main_dir%"
    git pull
    echo.
)

set /p update_dev=Update dev branch instance? (Y/N):
if /i "%update_dev%"=="Y" (
    echo Updating dev branch instance...
    cd /D "%dev_dir%"
    git pull
    echo.
)

set /p update_dev=Update SillyTavern Extras instance? (Y/N):
if /i "%update_dev%"=="Y" (
    echo Updating SillyTavern Extras instance...
    cd /D "%extras_dir%"
    git config --global --add safe.directory C:/%USERPROFILE%/Documents/SillyTavern-extras
    git pull
    echo.
)

echo.
echo Update process completed.
pause Press any key to exit...
