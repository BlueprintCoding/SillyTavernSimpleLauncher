@echo off

echo Stopping Node.js to Shutdown ST...
taskkill /f /im node.exe > nul 2>&1

echo Node servers for SillyTavern have been shut down.
pause
