# Installation and Uninstallation Scripts

This repository contains a set of Windows batch scripts to automate the installation and uninstallation of various software components. The scripts are designed to simplify the installation process and provide an easy way to uninstall the installed components.

THESE INSTALLERS COME WITH NO GUARANTEE OR WARRANTY, USE AT YOUR OWN RISK.

## Installation Script

The installation script (`install.bat`) allows you to install the following software components:

1. Chocolatey 
2. GIT
3. NVM (Node Version Manager)
4. Node.js LTS54. SillyTavern
6. SillyTavernExtras

The script checks if these components are already installed and skips the installation if they are found. If they are not present, it performs the following steps:

1. Installs GIT using Chocolatey package manager.
2. Installs NVM using Chocolatey package manager.
3. Uses NVM to install Node.js LTS version.
4. Clones the SillyTavern repository from GitHub to the user's Documents folder.
5. Prompts the user to choose between the main and dev branch of SillyTavern.
6. Runs the `Start.bat` script from the SillyTavern directory.

Please run the `install.bat` script with administrator privileges to ensure a successful installation.

## Uninstallation Script

The uninstallation script (`uninstall.bat`) provides a way to remove the installed components. It prompts the user to confirm the uninstallation of each component and performs the necessary cleanup.

The uninstall scripts allows you to remove the following components:

1. GIT
2. Node.js and NVM
3. Chocolatey
4. SillyTavern
5. SillyTavernExtras
6. Chocolatey 

For each component, the script asks for user confirmation before proceeding with the uninstallation. It also provides an option to delete the SillyTavernDevBranch directory if it exists.

Please run the `Uninstall SillyTavern.bat` script with administrator privileges and follow the prompts to uninstall the desired components.

## Usage

If any of the scripts fail, try running them again, sometimes your system may not initialize environmental variables correctly and running the script again can fix it. 

These scripts will ask for Administrator permissions, you must allow that for the install to work. Windows may also throw an unknown publisher warning, hit more info, then run anyway.

1. Place the "SillyTavernInstall" folder in your documents folder

2. Run the installation script (`Install SillyTavern - Run 1st.bat`) with administrator privileges to install the components.

3. When that finished running run the (`Install SillyTavern - Run 2nd.bat`) with administrator privileges to install the components.

4. When that finished running run the (`Run SillyTavern - Main Branch.bat`) or (`Run SillyTavern - Developer Preview Branch.bat`) depending which branch you want, with administrator privileges to install the components.

5. Optional: Run the installation script (`Update SillyTavern.bat`) to update the SillyTavern installs to the latest versions. This should preserve your chats and characters. 

6. Optional: Run the backup script (`Backup SillyTavern Files.bat`) to backup the SillyTavern: Backgrounds, Characters, Chats, Groups, Group chats, KoboldAI Settings, NovelAI Settings, OpenAI Settings, TextGen Settings, Themes, User Avatars, Worlds, settings.json 
	-  You can find the backup files in the "ST-Backups" folder in your Documents directory, organized by date and timestamp.

7. Optional: Run the installation script (`Install SillyTavernExtras - Optional.bat`) to install the SillyTavernExtra extensions. NOTE: You may have to run this script multiple times to finish installs after dependencies.

8. Optional: Run the uninstallation script (`Uninstall SillyTavern.bat`) and (`Uninstall SillyTavernExtras.bat`) with administrator privileges to remove the installed components.

Note: Please review the scripts and make any necessary modifications based on your specific requirements or system configurations.

