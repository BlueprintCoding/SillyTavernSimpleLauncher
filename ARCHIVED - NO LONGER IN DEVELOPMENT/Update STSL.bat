@echo off

REM Change directory to the root of your app
cd /d "%~dp0"

REM Perform a Git pull to update the repository
git pull

REM Pause the script to keep the command prompt window open
pause