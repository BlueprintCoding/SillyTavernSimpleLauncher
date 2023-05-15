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
    choco uninstall git -y
    rmdir /s /q "C:\Program Files\Git"
)

:: Uninstall NodeJS
echo Do you want to uninstall NodeJS? (Y/N)
set /P uninstallNode=
if /I "%uninstallNode%"=="Y" (
    echo Uninstalling NodeJS...
    
    :: Find currently installed version of Node
    for /f "tokens=*" %%A in ('nvm list') do (
        echo %%A | findstr /r /c:"^[^v]"
        if not errorlevel 1 (
            set "version=%%A"
            goto UninstallNode
        )
    )
    
    echo No NodeJS version found. Skipping uninstallation.
    goto UninstallNVM
    
    :UninstallNode
    echo Uninstalling NodeJS version: !version!...
    nvm uninstall !version!
    rem nvm off (commented out as it's not necessary in the uninstallation process)
)

:: Uninstall NVM
:UninstallNVM
echo Do you want to uninstall NVM? (Y/N)
set /P uninstallNvm=
if /I "%uninstallNvm%"=="Y" (
    echo Uninstalling NVM...
    choco uninstall nvm -y
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
