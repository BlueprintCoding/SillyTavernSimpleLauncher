@echo off
:: Get the path of the parent folder
for %%I in ("%~dp0..\..") do set "ParentFolder=%%~fI"

set main_dir=%ParentFolder%\SillyTavern-MainBranch
set dev_dir=%ParentFolder%\SillyTavern-DevBranch
set extras_dir=%ParentFolder%\SillyTavern-extras

echo Updating SillyTavern instances:
echo.

:PromptUpdateMain
set /p update_main=Do you want to backup your Character, Chats, etc? (Y/N):
if /i "%update_main%"=="Y" (
    echo Backing up files... Please wait to confirm backup in "\%ParentFolder%\ST-Backups"
    call "%~dp0Backup SillyTavern Files.bat"
    echo.
)

:PromptUpdateMainBranch
set /p update_main=Update main branch instance? (Y/N):
if /i "%update_main%"=="Y" (
    if exist "%main_dir%" (
        echo Updating main branch instance...
        cd /D "%main_dir%"
        git pull
    ) else (
        echo Main branch directory does not exist. Skipping update.
    )
    echo.
)

:PromptUpdateDevBranch
set /p update_dev=Update dev branch instance? (Y/N):
if /i "%update_dev%"=="Y" (
    if exist "%dev_dir%" (
        echo Updating dev branch instance...
        cd /D "%dev_dir%"
        git pull
    ) else (
        echo Dev branch directory does not exist. Skipping update.
    )
    echo.
)

:PromptUpdateExtras
set /p update_extras=Update SillyTavern Extras instance? (Y/N):
if /i "%update_extras%"=="Y" (
    if exist "%extras_dir%" (
        echo Updating SillyTavern Extras instance...
        cd /D "%extras_dir%"
        git config --global --add safe.directory C:/%ParentFolder%/SillyTavern-extras
        git pull
    ) else (
        echo SillyTavern Extras directory does not exist. Skipping update.
    )
    echo.
)

echo.
echo Update process completed.
pause Press any key to exit...
