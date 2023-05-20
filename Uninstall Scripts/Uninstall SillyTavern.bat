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

:: Uninstall GIT
echo Do you want to uninstall GIT? (Y/N)
set /P uninstallGit=
if /I "%uninstallGit%"=="Y" (
    echo Uninstalling GIT...
    choco uninstall git --yes
    rmdir /s /q "C:\Program Files\Git"
)

:: Load NVM environment
echo Loading NVM environment...
CALL "%SystemDrive%\ProgramData\nvm\nvm.exe" use 18

:: Uninstall Node.js
echo Do you want to uninstall Node.js? (Y/N)
set /P uninstallNode=
if /I "%uninstallNode%"=="Y" (
    echo Uninstalling Node.js...
    choco uninstall nodejs --yes

    echo Checking for Node.js installation in "C:\Program Files"...
    if exist "C:\Program Files\nodejs" (
        echo Node.js found in "C:\Program Files". Deleting directory...
        rmdir /s /q "C:\Program Files\nodejs"
		echo You may have orphaned NodeJS values in your Enviromental variables, you can manually remove those.
    ) else (
        echo Node.js is not installed in "C:\Program Files".
    )
)

:: Uninstall NVM
:UninstallNVM
echo Do you want to uninstall NVM? (Y/N)
set /P uninstallNvm=
if /I "%uninstallNvm%"=="Y" (
    echo Uninstalling NVM...
    choco uninstall nvm --yes
)


:: Uninstall Python Packages
echo Do you want to uninstall, pyperlcip, nltk, pillow? (Y/N)
set /P uninstallPP=
if /I "%uninstallPP%"=="Y" (
    echo Uninstalling Python imports...

REM Uninstall pyperclip
pip uninstall -y pyperclip

REM Uninstall nltk
pip uninstall -y nltk

REM Uninstall Pillow
pip uninstall -y pillow

)

:: Remove Chocolatey directory
echo Do you want to remove Chocolatey? (Y/N)
set /P removeChoco=
if /I "%removeChoco%"=="Y" (
    echo Removing Chocolatey directory...
    rmdir /s /q "C:\ProgramData\chocolatey"
)

:: Get the path of the parent folder
for %%I in ("%~dp0..\..") do set "ParentFolder=%%~fI"

:: Uninstall SillyTavern Main Branch
echo Do you want to uninstall the SillyTavern Main Branch? (Y/N)
set /P uninstallSillyTavern=
if /I "%uninstallSillyTavern%"=="Y" (
    echo Uninstalling SillyTavern...
    echo Deleting SillyTavern directory...
    rmdir /s /q "%ParentFolder%\SillyTavern-MainBranch"
)

:: Uninstall SillyTavern Dev Preview
echo Do you want to uninstall the SillyTavern Dev Preview? (Y/N)
set /P uninstallDevBranch=
if /I "%uninstallDevBranch%"=="Y" (
    echo Deleting SillyTavernDevBranch directory...
    rmdir /s /q "%ParentFolder%\SillyTavern-DevBranch"
)

echo Uninstallation completed successfully.
pause
