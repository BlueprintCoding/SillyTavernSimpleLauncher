# SillyTavern Extras Installation Script

This batch script automates the installation process for SillyTavern Extras, a collection of Python dependencies required for running the SillyTavernExtras server. The script installs the necessary packages and sets up the server for use.

## What does the script do?

1. Checks for administrative privileges and requests elevation if needed.
2. Installs Python 3.10 using Chocolatey if it's not already installed.
3. Clones the SillyTavern Extras repository into the user's Documents folder.
4. Installs the following dependencies using `pip`:
   - Flask
   - Flask-Cloudflared
   - Flask-CORS
   - Markdown
   - Pillow
   - colorama
   - webuiapi
   - torch (version 2.0.0+cu118)
   - torchvision (version 0.15.1)
   - torchaudio (version 2.0.1)
   - accelerate
   - transformers (version 4.28.1)
   - diffusers (version 0.16.1)
   - silero-api-server
5. Starts the SillyTavern server.

## Prerequisites

- Windows operating system
- Administrative privileges
- Internet connectivity

## Usage

1. Ensure you have administrative privileges.
2. Double-click the `Install SillyTavernExtras - Optional.bat` file to run the script.
3. Follow the prompts, if any, to install Python 3.10 and clone the SillyTavern Extras repository.
4. Wait for the script to install the required dependencies.
5. Once the installation is complete, the SillyTavern server will be started automatically.

## Uninstallation

To uninstall the installed dependencies and remove the SillyTavern Extras directory, run the `Uninstall SillyTavernExtras.bat` script. This script will uninstall each dependency and remove the directory from your system.

## Notes

- This script assumes you have Chocolatey installed for Python installation. Chocolatey should have been installed when you installed the main SillyTavern files.
- If you encounter any issues during the installation process, please check the prerequisites and ensure you have an active internet connection.
- For additional support or troubleshooting, refer to the SillyTavern documentation or contact the project maintainers.

