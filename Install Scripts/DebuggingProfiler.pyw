import platform
import subprocess
import os
import sys
import datetime
import json

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the log file path
log_file_path = os.path.join(script_directory, "..", "Logs", "DebuggingProfile.log")
repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "SillyTavern-MainBranch"))

def check_repository_updated(repo_dir):
    """
    Check if the local Git repository is updated to the current version.
    Returns True if the repository is up to date, False otherwise.
    """
    if not os.path.exists(repo_dir):
        return False, ""

    subprocess.run(["git", "-C", repo_dir, "remote", "update"])
    result = subprocess.run(["git", "-C", repo_dir, "status", "-uno"], capture_output=True, text=True)

    # Get the current version number from the local repository's package.json file
    package_file = os.path.join(repo_dir, "package.json")
    with open(package_file) as f:
        package_data = json.load(f)
        current_version = package_data.get("version", "")

    return "Your branch is up to date" in result.stdout, current_version

# Function to write the system information to the log file
def write_system_info_to_log():
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Open the log file in append mode
    with open(log_file_path, "a") as log_file:
        # Write the title and timestamp
        log_file.write("SillyTavern System Info\n")
        log_file.write(f"Log Updated: {timestamp}\n")

        # Activate the virtual environment
        activate_script = os.path.join(script_directory, "..", "venv", "Scripts", "activate.bat")
        activation_result = subprocess.run(activate_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the virtual environment activation was successful
        if activation_result.returncode == 0:
            log_file.write("Virtual Environment Activated Successfully\n\n")
        else:
            log_file.write("Failed to Activate Virtual Environment\n\n")

        # Check if the repository directory exists
        if os.path.exists(repo_dir):
            # Check the version of SillyTavern installed
            current_version = check_repository_updated(repo_dir)
            log_file.write(f"SillyTavern Installed Version: {current_version}\n\n")

        # Write the operating system version
        os_version = platform.platform()
        log_file.write(f"Operating System Version: {os_version}\n")

        # Check if NodeJS is installed and get the version
        try:
            node_version = subprocess.check_output(["node", "--version"], stderr=subprocess.STDOUT, text=True)
            log_file.write(f"NodeJS Installed and Version: {node_version}")
        except subprocess.CalledProcessError:
            log_file.write("NodeJS is not installed\n")

        # Check if Chocolatey is installed
        try:
            choco_version = subprocess.check_output(["choco", "--version"], stderr=subprocess.STDOUT, text=True)
            log_file.write(f"Chocolatey Installed and Version: {choco_version}")
        except subprocess.CalledProcessError:
            log_file.write("Chocolatey is not installed\n")

        # Check if GIT is installed and get the version
        try:
            git_version = subprocess.check_output(["git", "--version"], stderr=subprocess.STDOUT, text=True)
            log_file.write(f"GIT Installed and Version: {git_version}")
        except subprocess.CalledProcessError:
            log_file.write("GIT is not installed\n")

        # Check if PIP is installed and get the version
        try:
            pip_version = subprocess.check_output(["pip", "--version"], stderr=subprocess.STDOUT, text=True)
            # Extract only the version number
            pip_version = pip_version.split(" ")[-1].strip()
            log_file.write(f"PIP Installed and Version: {pip_version}\n")
        except subprocess.CalledProcessError:
            log_file.write("PIP is not installed\n")

        # Check if specific Python packages are installed
        required_packages = ["Pillow", "pywin32", "pyperclip", "nltk"]
        installed_packages = subprocess.check_output(["pip", "list"], universal_newlines=True)
        for package in required_packages:
            if package in installed_packages:
                log_file.write(f"{package} is installed\n")
            else:
                log_file.write(f"{package} is not installed\n")

        # Add a break line
        log_file.write("---------------------------------------\n")

# Call the function to write the system information to the log file
write_system_info_to_log()
