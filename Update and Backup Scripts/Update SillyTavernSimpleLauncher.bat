@echo off
:: Get the path of the parent folder
for %%I in ("%~dp0..\..") do set "ParentFolder=%%~fI"

set main_dir=%ParentFolder%\SillyTavernSimpleLauncher

echo Updating SillyTavernSimpleLauncher instance:
echo.

:PromptUpdateMain
set /p update_main=Do you want to backup your Character, Chats, etc? (Y/N):
if /i "%update_main%"=="Y" (
    echo Backing up files... Please wait to confirm backup in "\%ParentFolder%\ST-Backups"
    call "%~dp0Backup SillyTavern Files.bat"
    echo.
)

:PromptUpdateMainBranch
set /p update_main=Update the SillyTavernSimpleLauncher instance? (Y/N):
if /i "%update_main%"=="Y" (
    if exist "%main_dir%" (
        echo Updating from the main branch...
        cd /D "%main_dir%"
        git pull
    ) else (
        echo Main branch directory does not exist. Skipping update.
    )
    echo.
)

echo.
echo Update process completed.
pause Press any key to exit...
