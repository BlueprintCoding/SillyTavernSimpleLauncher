# SillyTavernSimpleLauncher
A launcher that let's you install, uninstall, update, backup and uninstall SillyTavern and SillyTavernExtras

This repository contains a set of Windows batch scripts to automate the installation and uninstallation of various software components. The scripts are designed to simplify the installation process and provide an easy way to uninstall the installed components.

THESE INSTALLERS COME WITH NO GUARANTEE OR WARRANTY, USE AT YOUR OWN RISK.

## Usage

### To install this, download the zip from this github, move it to your documents folder, unzip it and follow the scripts below.
https://github.com/BlueprintCoding/SillyTavernSimpleLauncher/releases
OR
If you have GIT installed you can go to the directory that you want to install the Launcher in and run the following command
	git clone https://github.com/BlueprintCoding/SillyTavernSimpleLauncher -b main 

If any of the scripts fail, try running them again, sometimes your system may not initialize environmental variables correctly and running the script again can fix it. 

These scripts will ask for Administrator permissions, you must allow that for the install to work. Windows may also throw an unknown publisher warning, hit more info, then run anyway.

1. Place the "SillyTavernSimpleLauncher" folder in your desired install folder. Ex: your documents folder.
2. Follow the Installation Script instructions below. 
3. After installing you can use the "Launch SillyTavern and Extras.bat" to launch SillyTavern and SillyTavernExtras. It will prompt you to choose which branch of ST you want to launch and if you want to launch extras. 

Note: Please review the scripts and make any necessary modifications based on your specific requirements or system configurations.


## Installation Scripts (In the Install Scripts folder)
RUN THESE SCRIPTS IN ORDER! SillyTavern will be installed in the parent folder of the "SillyTavernSimpleLauncher" ex if you placed it in your Documents folder SillyTavern will be installed in the documents folder. 

SCRIPT1: "1 - Install SillyTavern Dependencies - Run 1st.bat"
----
Installs:
1. Chocolatey 
2. GIT
3. NVM (Node Version Manager)

After the script finishes running close the command prompt and run the next script
----

SCRIPT2: "2 - Install SillyTavern Dependencies - Run 2nd.bat"
----
Installs:
1. NodeJS

After the script finishes running close the command prompt.
You know can have two choices, 
-you can install the stable Main Branch of SillyTavern by running the script:
 	3a - Install SillyTavern - Main Branch.bat
AND/OR
-you can install the stable Main Branch of SillyTavern by running the script:
	3b - Install SillyTavern - Developer Preview Branch.bat
----

SCRIPT3a: "3a - Install SillyTavern - Main Branch.bat"
----
Installs:
1. Creates a directory called "SillyTavern-MainBranch" in the parent folder of "SillyTavernSimpleLauncher"
2. Clones "https://github.com/Cohee1207/SillyTavern -b main" to that folder
3. Launches SillyTavern by calling the "Start.bat" file
---

SCRIPT3b: "3b - Install SillyTavern - Developer Preview Branch.bat"
----
Installs:
1. Creates a directory called "SillyTavern-DevBranch" in the parent folder of "SillyTavernSimpleLauncher"
2. Clones "https://github.com/Cohee1207/SillyTavern -b dev" to that folder
3. Launches SillyTavern by calling the "Start.bat" file
---

SCRIPT4: "4 - Install SillyTavernExtras - Optional.bat"
----
Installs:
1. Checks to see if you have python 3.10 or above installed and installs it if you do not
2. Creates a directory called "SillyTavern-extras" in the parent folder of "SillyTavernSimpleLauncher"
3. Clones "https://github.com/Cohee1207/SillyTavern-extras" to that folder
4. Creates a virtual enviroment via venv in the "SillyTavern-extras" folder and installs all of the dependencies from requirements.txt there.
5. Activates the virtual enviroment
6. Launches SillyTavernExtras server (the first run can take some time as it installs additional dependencies)
---

----------------------------------------------------------------

## Uninstallation Scripts (In the Uninstall Scripts folder)

The uninstallation scripts provide a way to remove the installed components. It prompts the user to confirm the uninstallation of each component and performs the necessary cleanup.

SCRIPT1: "Uninstall SillyTavern.bat"
----
The uninstall scripts allows you to remove the following components (be advised removing dependencies like GIT, NodeJS and NVM can effect other programs on your computer if they depend on them) For each component, the script asks for user confirmation before proceeding with the uninstallation. :

1. GIT
2. NodeJS
3. NVM
4. Chocolatey
5. SillyTavern-MainBranch
6. SillyTavern-DevBranch

After the script finishes running close the command prompt 
----

SCRIPT2: "Uninstall SillyTavernExtras.bat"
----
The uninstall scripts allows you to remove the following components: 

1. venv virtual enviroment with dependencies
2. SillyTavern-extras

After the script finishes running close the command prompt 
----

----------------------------------------------------------------



