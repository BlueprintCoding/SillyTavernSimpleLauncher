# SillyTavernSimpleLauncher
A GUI launcher that let's you install, uninstall, update, backup and uninstall SillyTavern and SillyTavernExtras

This repository contains a set of Windows batch scripts and python files to automate the installation and uninstallation of various software components. The scripts are designed to simplify the installation process and provide an easy way to uninstall the installed components.

THESE INSTALLERS COME WITH NO GUARANTEE OR WARRANTY, USE AT YOUR OWN RISK.

## Usage

### To install this, download the zip from this github, move it to the folder of your choice, unzip it and follow the scripts below.
https://github.com/BlueprintCoding/SillyTavernSimpleLauncher/releases
OR
If you have GIT installed you can go to the directory that you want to install the Launcher in and run the following command
	git clone https://github.com/BlueprintCoding/SillyTavernSimpleLauncher -b main 

If any of the scripts fail, try running them again, sometimes your system may not initialize environmental variables correctly and running the script again can fix it. 

These scripts will ask for Administrator permissions, you must allow that for the install to work. Windows may also throw an unknown publisher warning, hit more info, then run anyway.

1. Place the "SillyTavernSimpleLauncher" folder in your desired install folder. Ex: your documents folder.
2. Follow the Installation Script instructions below. 
3. After installing you can use the GUI to install, manage, and uninstall Sillytavern and Extras. It also includes some tools like configurations editing and prompt optimization. 

Note: Please review the scripts and make any necessary modifications based on your specific requirements or system configurations.


## Installation Scripts (In the Install Scripts folder)
RUN THESE SCRIPTS IN ORDER! SillyTavern will be installed in the parent folder of the "SillyTavernSimpleLauncher" ex if you placed it in your Documents folder SillyTavern will be installed in the documents folder. 

SCRIPT1: "RUN FIRST Install GUI Dependencies.bat"
----
Installs:
1. Chocolatey 
2. GIT
3. NVM (Node Version Manager)
4. Python (imports Pillow, Tkinter, win32api)

After the script finishes running close the command prompt and run the next script
----

SCRIPT2: "RunGUI-Launcher.bat"
----
Installs:
1. Nothing! Just checks that the required dependencies are installed and launches the Launcher GUI"
----

Launcher GUI: "STLauncherGui.py"
----
Install Scripts:
The launcher has buttons to Install SillyTavern and Extras. Make sure to launch them in order from top to bottom, waiting for each to finish before launching the next. 
Command windows will open when you hit run, some may require Administrator access, allow that or it will not work.

--

Tools:
The launcher has buttons to:
1) Backup your SillyTavern files: Backs up file such as chats and characters, they will save in the parent directory in a folder called "SillyTavern-FileBackups"
2) Update SillyTavern: Gives you the option to update the main and dev branches of SillyTavern to the latest version for the repo using GIT Pull
3) Update SillyTavern: Gives you the option to update the SillyTavern Simple Launcher to the latest version for the repo using GIT Pull
4) OptimizePrompt Gui: Opens a new window to allow you to run a stemming function on your prompts/char info to reduce the size. Works best for OpenAI and Poe api

--

Uninstall Script:
1)Uninstall SillyTavern: gives you options to uninstall both branches of SillyTavern and their dependencies
2)Uninstall SillyTavern: gives you options to uninstall SillyTavern Extras

--

Support:
Links that open your web browser to various support resources

--

Install Paths:
Checks your system to show where SillyTavern, Extras, and Backups are currently installed.
----

----------------------------------------------------------------

