@echo off
:: Get the path of the parent folder
for %%I in ("%~dp0..\..") do set "ParentFolder=%%~fI"

set main_dir=%ParentFolder%\SillyTavernSimpleLauncher

echo Updating SillyTavernSimpleLauncher instance:
echo.
echo We recommend running the backup function before updating. 

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
