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

REM Uninstall dependencies

REM Uninstall Flask
echo Uninstalling Flask...
python -m pip uninstall -y flask

REM Uninstall Flask-Cloudflared
echo Uninstalling Flask-Cloudflared...
python -m pip uninstall -y flask-cloudflared

REM Uninstall Flask-CORS
echo Uninstalling Flask-CORS...
python -m pip uninstall -y flask-cors

REM Uninstall Markdown
echo Uninstalling Markdown...
python -m pip uninstall -y markdown

REM Uninstall Pillow
echo Uninstalling Pillow...
python -m pip uninstall -y Pillow

REM Uninstall colorama
echo Uninstalling colorama...
python -m pip uninstall -y colorama

REM Uninstall webuiapi
echo Uninstalling webuiapi...
python -m pip uninstall -y webuiapi

REM Uninstall torch, torchvision, torchaudio
echo Uninstalling torch, torchvision, torchaudio...
python -m pip uninstall -y torch torchvision torchaudio

REM Uninstall accelerate
echo Uninstalling accelerate...
python -m pip uninstall -y accelerate

REM Uninstall transformers
echo Uninstalling transformers...
python -m pip uninstall -y transformers

REM Uninstall diffusers
echo Uninstalling diffusers...
python -m pip uninstall -y diffusers

REM Uninstall silero-api-server
echo Uninstalling silero-api-server...
python -m pip uninstall -y silero-api-server

REM Remove the SillyTavern-extras directory
echo Removing the SillyTavern-extras directory...
RD /S /Q "C:\Users\dev\Documents\SillyTavern-extras"

echo Uninstallation completed.

pause
