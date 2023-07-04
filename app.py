import subprocess
import shutil
import os
import re
import logging
from flask import Flask, render_template, request, jsonify, redirect
from datetime import datetime
import socket
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string
import traceback
import requests
from tqdm import tqdm
import time
import threading
from config import APP_VERSION

app = Flask(__name__)
home_folder = os.path.dirname(os.path.abspath(__file__))
# Get the full path to the taskkill executable
taskkill_executable = os.path.join(os.environ['WINDIR'], 'System32', 'taskkill.exe')
# Get the parent directory of the current script file
script_directory = os.path.dirname(os.path.abspath(__file__))


# Create the Logs folder if it doesn't exist
logs_folder = os.path.join(script_directory, "Logs")
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)

# Configure logging
log_file_path = os.path.join(logs_folder, "STSL.log")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and set its level to DEBUG
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the file handler
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# def get_external_ip():
#     response = requests.get('https://api.ipify.org?format=json')
#     data = response.json()
#     ip_address = data['ip']
#     return ip_address


def check_repos_cloned():
    parent_folder = os.path.abspath(os.path.join(app.root_path, ".."))
    sillytavern_main_path = os.path.join(parent_folder, "SillyTavern-MainBranch")
    sillytavern_dev_path = os.path.join(parent_folder, "SillyTavern-DevBranch")
    sillytavern_extras_path = os.path.join(parent_folder, "SillyTavern-extras")

    repos_cloned = {
        'main': os.path.exists(sillytavern_main_path),
        'dev': os.path.exists(sillytavern_dev_path),
        'extras': os.path.exists(sillytavern_extras_path),
    }

    return repos_cloned


def copy_instance_files(source, destination):
    public_folder = os.path.join(source, "public")

    if not os.path.exists(public_folder):
        logging.error("Public folder not found in the source directory.")
        return

    dirs_to_copy = [
        "Backgrounds", "Characters", "Chats", "Group chats", "Groups",
        "KoboldAI Settings", "NovelAI Settings", "OpenAI Settings",
        "TextGen Settings", "Themes", "User Avatars", "Worlds"
    ]
    files_to_copy = ["settings.json"]

    for dir_to_copy in dirs_to_copy:
        source_dir = os.path.join(public_folder, dir_to_copy)
        destination_dir = os.path.join(destination, dir_to_copy.replace(" ", "_"))

        if os.path.exists(source_dir):
            if os.path.exists(destination_dir):
                shutil.rmtree(destination_dir)
            try:
                shutil.copytree(source_dir, destination_dir)
                logging.info(f"Directory copied: {source_dir} -> {destination_dir}")
            except Exception as e:
                logging.error(f"Failed to copy directory: {source_dir}\nError: {str(e)}")
        else:
            logging.info(f"Source directory not found: {source_dir}")

    for file_to_copy in files_to_copy:
        source_file = os.path.join(public_folder, file_to_copy)
        destination_file = os.path.join(destination, file_to_copy)

        if os.path.exists(source_file):
            try:
                shutil.copy2(source_file, destination_file)
                logging.info(f"File copied: {source_file} -> {destination_file}")
            except Exception as e:
                logging.error(f"Failed to copy file: {source_file}\nError: {str(e)}")
        else:
            logging.info(f"Source file not found: {source_file}")


@app.route("/")
def index():
    # Check if SillyTavern MainBranch exists
    parent_folder = os.path.abspath(os.path.join(home_folder, ".."))
    sillytavern_main_path = os.path.join(parent_folder, "SillyTavern-MainBranch")
    sillytavern_main_exists = os.path.exists(sillytavern_main_path)

    # Check if SillyTavern DevBranch exists
    sillytavern_dev_path = os.path.join(parent_folder, "SillyTavern-DevBranch")
    sillytavern_dev_exists = os.path.exists(sillytavern_dev_path)

    # Check if SillyTavern Extras exists
    sillytavern_extras_path = os.path.join(parent_folder, "SillyTavern-extras")
    sillytavern_extras_exists = os.path.exists(sillytavern_extras_path)

    # Check if repositories are cloned
    repos_cloned = check_repos_cloned()

    # Get latest repo release number
    def get_latest_release():
        url = "https://api.github.com/repos/BlueprintCoding/SillyTavernSimpleLauncher/releases/latest"
        response = requests.get(url)
        if response.status_code == 200:
            release_data = response.json()
            return release_data["tag_name"]
        else:
            return None

    latest_release = get_latest_release()


    return render_template('index.html', repos_cloned=repos_cloned, app_version=APP_VERSION,latest_release=latest_release)


@app.route("/migrate-profile", methods=["GET"])
def migrate_profile_manager():
    return render_template("migrate.html")


@app.route("/migrate-instance", methods=["POST"])
def migrate_instance():
    source_directory = request.form.get("source_directory")
    new_instance_name = request.form.get("new_instance_name")
    branch_choice_var = request.form.get("branch_choice")

    if not source_directory or not new_instance_name or not branch_choice_var:
        return "Invalid form data. Please fill in all the fields."

    # Validate source directory
    if not os.path.isdir(source_directory):
        return "Invalid source directory."

    # Prepare destination directory
    destination_directory = os.path.abspath(os.path.join(script_directory, "..", "SillyTavern-Instances"))
    new_instance_folder = os.path.join(destination_directory, f"{new_instance_name}-{branch_choice_var}")

    if os.path.exists(new_instance_folder):
        return f"Profile '{new_instance_name}-{branch_choice_var}' already exists."

    try:
        os.makedirs(new_instance_folder)  # Create the new instance folder
        migrate_instance_files(source_directory, new_instance_folder)
        logging.info(f"New profile created: {new_instance_name}-{branch_choice_var}")

        # Return a JSON response indicating success
        return jsonify({"success": True,
                        "message": f"New profile '{new_instance_name}-{branch_choice_var}' created successfully."})

    except Exception as e:
        logging.error(str(e))

        # Return a JSON response indicating error
        return jsonify({"success": False, "message": f"Error creating the new profile: {str(e)}"})


def migrate_instance_files(source_directory, destination_directory):
    # Files and folders to copy, located inside the "public" folder of the source_directory
    dirs_to_copy = [
        "Backgrounds", "Characters", "Chats", "Group chats", "Groups",
        "KoboldAI Settings", "NovelAI Settings", "OpenAI Settings",
        "TextGen Settings", "Themes", "User Avatars", "Worlds"
    ]
    files_to_copy = ["settings.json"]

    source_public_directory = os.path.join(source_directory, "public")

    # Copy directories
    for directory in dirs_to_copy:
        source_dir = os.path.join(source_public_directory, directory)
        if os.path.isdir(source_dir):
            destination_dir = os.path.join(destination_directory, directory)
            os.makedirs(destination_dir)  # Create the destination directory
            print(f"Copying directory: {source_dir} -> {destination_dir}")
            for file_name in os.listdir(source_dir):
                source_file = os.path.join(source_dir, file_name)
                destination_file = os.path.join(destination_dir, file_name)
                if os.path.isfile(source_file):
                    shutil.copy2(source_file, destination_file)
                    print(f"Copied file: {source_file} -> {destination_file}")

    # Copy files
    for file in files_to_copy:
        source_file = os.path.join(source_public_directory, file)
        if os.path.isfile(source_file):
            destination_file = os.path.join(destination_directory, file)
            shutil.copy2(source_file, destination_file)
            print(f"Copied file: {source_file} -> {destination_file}")


@app.route('/optimize-prompt')
def optimize_prompt():
    return render_template('optimize_prompt.html')


@app.route("/launch-main", methods=['POST'])
def launch_main():
    branch_name = "SillyTavern-MainBranch"
    start_script_dir = os.path.abspath(os.path.join(home_folder, "..", branch_name))
    start_script_path = os.path.join(start_script_dir, "Start.bat")
    subprocess.Popen(start_script_path, shell=True)
    app_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the port values from the config files
    config_file_path_main = os.path.join(app_dir, '..', 'SillyTavern-MainBranch', 'config.conf')
    port_main = parse_config_file(config_file_path_main).get('port')
    return jsonify(message="Launching ST Main...", port=port_main)


@app.route("/launch-dev", methods=['POST'])
def launch_dev():
    branch_name = "SillyTavern-DevBranch"
    start_script_dir = os.path.abspath(os.path.join(home_folder, "..", branch_name))
    start_script_path = os.path.join(start_script_dir, "Start.bat")
    subprocess.Popen(start_script_path, shell=True)
    app_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the port values from the config files
    config_file_path_dev = os.path.join(app_dir, '..', 'SillyTavern-DevBranch', 'config.conf')
    port_dev = parse_config_file(config_file_path_dev).get('port')
    return jsonify(message="Launching ST Dev...", port=port_dev)


# List of available modules
modules = [
    "caption",
    "summarize",
    "classify",
    "sd",
    "silero-tts",
    "edge-tts",
    "chromadb"
]

@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    # Read the config.conf file based on the selected branch
    app_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path_main = os.path.join(app_dir, '..', 'SillyTavern-MainBranch', 'config.conf')
    config_file_path_dev = os.path.join(app_dir, '..', 'SillyTavern-DevBranch', 'config.conf')

    # Parse the config.conf files and extract the default values
    default_values_main = {}
    default_values_dev = {}
    main_installed = ""
    dev_installed = ""

    if os.path.isfile(config_file_path_main):
        default_values_main = parse_config_file(config_file_path_main)
        print(f"Main: {default_values_main} ")
        main_installed = "main"
    if os.path.isfile(config_file_path_dev):
        default_values_dev = parse_config_file(config_file_path_dev)
        print(f"Dev: {default_values_dev}")
        dev_installed = "dev"

    if main_installed == "" and dev_installed == "":
        print("Dev and Main not installed")
        return "No SillyTavern Install found, please install main or dev"
    elif main_installed == "main" and dev_installed == "":
        # Pass the main values to the HTML template
        print("Main Installed, Dev Not")
        return render_template('edit_config.html', default_values_main=default_values_main,
                               default_values_dev={})
    elif main_installed == "" and dev_installed == "dev":
        # Pass the dev values to the HTML template
        print("Dev Installed, Main Not")
        return render_template('edit_config.html', default_values_main={},
                               default_values_dev=default_values_dev)
    elif main_installed == "main" and dev_installed == "dev":
        # Pass both branch values to the HTML template
        print("Dev and Main installed")
        return render_template('edit_config.html', default_values_main=default_values_main,
                               default_values_dev=default_values_dev)


def parse_config_file(file_path):
    default_values = {}
    with open(file_path, 'r') as config_file:
        config_content = config_file.read()
        pattern = r"const\s+(\w+)\s+=\s+(.*?);"
        matches = re.findall(pattern, config_content, re.MULTILINE)
        for key, value in matches:
            try:
                if key == "basicAuthUser":
                    # Extract the username and password values using regular expressions
                    username_match = re.search(r'username: "([^"]+)"', value)
                    password_match = re.search(r'password: "([^"]+)"', value)
                    username = username_match.group(1) if username_match else ""
                    password = password_match.group(1) if password_match else ""
                    default_values[key] = {
                        'username': username,
                        'password': password
                    }
                else:
                    default_values[key] = eval(value)
            except:
                default_values[key] = value
    return default_values


@app.route('/config-update', methods=['POST'])
def update_configuration():
    branch = request.form['branch']
    port = request.form['port']
    whitelist = request.form['whitelist']
    whitelist_mode = request.form.get('whitelistMode', False)
    basic_auth_mode = request.form.get('basicAuthMode', False)
    basic_auth_username = request.form['basicAuthUsername']
    basic_auth_password = request.form['basicAuthPassword']
    disable_thumbnails = request.form.get('disableThumbnails', False)
    autorun = request.form.get('autorun', False)
    enable_extensions = request.form.get('enableExtensions', False)
    listen = request.form.get('listen', False)
    allow_keys_exposure = request.form.get('allowKeysExposure', False)

    # Read the config.conf file based on the selected branch
    app_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path_main = os.path.join(app_dir, '..', 'SillyTavern-MainBranch', 'config.conf')
    config_file_path_dev = os.path.join(app_dir, '..', 'SillyTavern-DevBranch', 'config.conf')

    # Set the configuration file path based on the branch selection
    if branch == "Select Branch":
        return 'Error: Select a branch.'
    elif branch == "Main Branch":
        config_file = config_file_path_main
    elif branch == "Dev Branch":
        config_file = config_file_path_dev
    else:
        return 'Error: Invalid branch selection.'

    # Read the existing config file
    with open(config_file, "r") as f:
        config_content = f.readlines()

    # Update the configuration values in the config content
    updated_content = []
    for line in config_content:
        if line.startswith("const port"):
            updated_content.append(f"const port = {port};\n")
        elif line.startswith("const whitelist ="):
            updated_content.append(f"const whitelist = ['{whitelist}']; //{line.split('//', 1)[1]}")
        elif line.startswith("const whitelistMode"):
            updated_content.append(f"const whitelistMode = {str(whitelist_mode).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const basicAuthMode"):
            updated_content.append(f"const basicAuthMode = {str(basic_auth_mode).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const basicAuthUser"):
            updated_content.append(
                f"const basicAuthUser = {{username: \"{basic_auth_username}\", password: \"{basic_auth_password}\"}}; //{line.split('//', 1)[1]}")
        elif line.startswith("const disableThumbnails"):
            updated_content.append(
                f"const disableThumbnails = {str(disable_thumbnails).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const autorun"):
            updated_content.append(f"const autorun = {str(autorun).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const enableExtensions"):
            updated_content.append(
                f"const enableExtensions = {str(enable_extensions).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const listen"):
            updated_content.append(f"const listen = {str(listen).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const allowKeysExposure"):
            updated_content.append(
                f"const allowKeysExposure = {str(allow_keys_exposure).lower()}; //{line.split('//', 1)[1]}")
        else:
            updated_content.append(line)

    # Write the updated config content to the file
    with open(config_file, "w") as f:
        f.writelines(updated_content)

    # Return JavaScript code to display an alert
    return '''
    <script>
        alert('Configuration updated successfully');
        window.location.href = '/configuration'; // Redirect to the configuration page
    </script>
    '''


@app.route("/close-sillytavern", methods=['POST'])
def close_sillytavern():
    os.system(f'"{taskkill_executable}" /f /im node.exe')
    return "Closing ST..."

@app.route("/shutdown-stsl", methods=['GET', 'POST'])
def shutdown_servers():
    # Terminate Node.js servers
    node_servers = []
    try:
        result = subprocess.run(['taskkill', '/im', 'node.exe', '/f'], capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            node_servers.append("Node.js servers")
            print("Node.js servers terminated successfully.")
        else:
            print("No Node.js servers found.")
    except subprocess.TimeoutExpired:
        print("Terminating Node.js servers timed out.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while terminating Node.js servers: {e}")

    # Terminate Python servers
    python_servers = []
    try:
        subprocess.run(['taskkill', '/im', 'python.exe', '/f'], timeout=2)
        python_servers.append("Python servers")
        print("Python servers terminated successfully.")
    except subprocess.TimeoutExpired:
        print("Terminating Python servers timed out.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while terminating Python servers: {e}")

    response_data = {
        "node_servers": node_servers,
        "python_servers": python_servers,
    }

    return jsonify(response_data)



@app.route("/install-main-branch", methods=['GET', 'POST'])
def install_main_branch():
    parent_folder = os.path.abspath(os.path.join(home_folder, ".."))
    sillytavern_path = os.path.join(parent_folder, "SillyTavern-MainBranch")

    # Check if SillyTavern is already installed
    if os.path.exists(sillytavern_path):
        return "SillyTavern Main is already installed, skipping installation."
    else:
        # Clone SillyTavern repository
        clone_command = [
            "git", "clone", "https://github.com/SillyTavern/SillyTavern", "-b", "main", sillytavern_path
        ]
        subprocess.run(clone_command)
        return 'SillyTavern Main Branch installed successfully.'


@app.route("/install-dev-branch", methods=['GET', 'POST'])
def install_dev_branch():
    parent_folder = os.path.abspath(os.path.join(home_folder, ".."))
    sillytaverndev_path = os.path.join(parent_folder, "SillyTavern-DevBranch")

    # Check if SillyTavern is already installed
    if os.path.exists(sillytaverndev_path):
        return "SillyTavern Dev is already installed, skipping installation."
    else:
        # Clone SillyTavern repository
        clone_command = [
            "git", "clone", "https://github.com/SillyTavern/SillyTavern.git", "-b", "dev", sillytaverndev_path
        ]
        subprocess.run(clone_command)

        return 'SillyTavern Dev Branch installed successfully.'



# Define shared path/directory variables as global
parent_folder = os.path.abspath(os.path.join(home_folder, ".."))
sillytavern_extras_path = os.path.join(parent_folder, "SillyTavern-extras")
venv_path = os.path.join(sillytavern_extras_path, "venv")


@app.route('/extras-manager', methods=['POST', 'GET'])
def extras_manager():
    global sillytavern_extras_path, venv_path

    if request.method == 'POST':
        selected_modules = request.form.getlist('modules')
        custom_flags = request.form.get('custom_flags')
        emotions_flag = request.form.getlist('emotions28')
        listen_flag = request.form.getlist('listen')

        launch_extras = True
        start_extras(launch_extras, selected_modules, emotions_flag, listen_flag, custom_flags)

        return redirect('/')
    else:
        if not os.path.exists(sillytavern_extras_path) or not os.path.exists(venv_path):
            alert_message = "Please install SillyTavern Extras first."
            return render_template('index.html', alert_message=alert_message)

        return render_template('extras_manager.html')


@app.route("/install-extras", methods=['GET', 'POST'])
def install_extras():
    global sillytavern_extras_path, venv_path

    try:
        if not sillytavern_extras_path or not venv_path:
            return 'Error: SillyTavern Extras path not found.'

        if os.path.exists(sillytavern_extras_path):
            logger.info("SillyTavern-extras is already installed. Skipping clone...")
            return 'SillyTavern Extras is already installed.'

        subprocess.run(["git", "clone", "https://github.com/SillyTavern/SillyTavern-extras", sillytavern_extras_path])

        venv_path = os.path.join(sillytavern_extras_path, "venv")

        if not os.path.exists(venv_path):
            subprocess.run(["python", "-m", "venv", venv_path])

        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
        subprocess.run([activate_script], shell=True, text=True)

        subprocess.run([os.path.join(venv_path, "Scripts", "python"), "-m", "pip", "install", "--upgrade", "pip"])

        requirements_file = os.path.join(sillytavern_extras_path, "requirements-complete.txt")
        subprocess.run(
            [os.path.join(venv_path, "Scripts", "pip"), "install", "--no-cache-dir", "-r", requirements_file])

        return "SillyTavern Extras installed successfully."

    except Exception as e:
        logger.error(f"Error in install_extras function: {e}")
        logger.exception("An error occurred during installation.")

        return 'An error occurred during Extras installation.'


def start_extras(launch_extras, selected_modules, emotions_flag, listen_flag, custom_flags):
    global sillytavern_extras_path, venv_path, stable_diffusion_dir

    try:
        if not sillytavern_extras_path or not venv_path:
            return 'Error: SillyTavern Extras path not found.'

        if launch_extras:
            enabled_modules_arg = "--enable-modules=" + ",".join(selected_modules)

            if emotions_flag:
                enabled_modules_arg += ",classify"
                enabled_modules_arg += " --classification-model=joeddav/distilbert-base-uncased-go-emotions-student"

            if listen_flag:
                enabled_modules_arg += " --listen"

            if custom_flags:
                enabled_modules_arg += " " + custom_flags

            activate_venv = os.path.abspath(os.path.join(venv_path, "Scripts", "activate.bat"))
            extras_port = "--port=5100"
            extras_path = os.path.join(sillytavern_extras_path, "server.py")
            venv_python = os.path.join(venv_path, "Scripts", "python.exe")
            stable_diffusion_dir = os.path.join(home_folder, "StableDiffusion")

            if os.path.exists(venv_python):
                logger.debug("Virtual environment exists.")
            if os.path.exists(extras_path):
                logger.debug("Extras path exists.")

            # Execute webui.bat if "sd" module is selected
            if "sd" in selected_modules:
                webui_bat_path = os.path.join(stable_diffusion_dir, "webui-user.bat")
                print(webui_bat_path)

                # Change the working directory to the StableDiffusion folder
                os.chdir(stable_diffusion_dir)

                # Start StableDiffusion in a new shell using a separate thread
                stable_diffusion_thread = threading.Thread(target=lambda: subprocess.run([webui_bat_path], shell=True))
                stable_diffusion_thread.start()

                # Wait for StableDiffusion to finish loading
                wait_for_stable_diffusion()

            process = subprocess.Popen(
                ['start', 'cmd', '/k',
                 f'call {activate_venv} && {venv_python} {extras_path} {enabled_modules_arg} {extras_port}'],
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

            print('start', 'cmd', '/k',
                  f'call {activate_venv} && {venv_python} {extras_path} {enabled_modules_arg} {extras_port}')
            # Retrieve the PID of the server process
            server_pid = process.pid
            logger.info("Server launched successfully.")

            # Return the server PID
            return server_pid

        else:
            return "SillyTavern-extras Installed..."

    except Exception as e:
        logger.error(f"Error in install_extras function: {e}")
        logger.exception("An error occurred during installation.")

        return 'Error: An error occurred during installation.'


def wait_for_stable_diffusion():
    url = "http://127.0.0.1:7860/"

    # Check if StableDiffusion web UI is accessible
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(1)  # Wait for 1 second before retrying


@app.route("/install", methods=['POST'])
def install():
    module = request.get_data(as_text=True)

    if module == "dependencies":
        # Install SillyTavern Dependencies
        return install_dependencies()

    elif module == "mainBranch":
        # Install SillyTavern - Main Branch
        return install_main_branch()

    elif module == "devBranch":
        # Install SillyTavern - Developer Preview Branch
        return install_dev_branch()

    elif module == "extras":
        # Install SillyTavernExtras
        return install_extras()

    else:
        return "Invalid module selection"

    # Return a response indicating successful installation
    return "Installation completed successfully"


@app.route('/backup-sillytavern-files', methods=['POST'])
def backup_sillytavern_files():
    # Get the path of the parent folder
    parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Create the ST-Backups folder if it doesn't exist
    backup_folder = os.path.join(parent_folder, 'SillyTavern-FileBackups')
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # Create a dated directory with timestamp for the copied files
    timestamp = datetime.now().strftime('%H%M%S')  # Format: HHMMSS
    datestamp = datetime.now().strftime('%Y%m%d')  # Format: YYYYMMDD

    # Backup from SillyTavern-MainBranch
    main_branch = os.path.join(parent_folder, 'SillyTavern-MainBranch\public')
    main_destination_folder = os.path.join(backup_folder, 'MainBranch', f'{datestamp}_{timestamp}')
    if os.path.exists(main_branch):
        os.makedirs(main_destination_folder)
        copy_files(main_branch, main_destination_folder, [
            'Backgrounds',
            'Characters',
            'Chats',
            'Groups',
            'Group chats',
            'KoboldAI Settings',
            'NovelAI Settings',
            'OpenAI Settings',
            'TextGen Settings',
            'Themes',
            'User Avatars',
            'Worlds',
            'settings.json'
        ])
    else:
        print('MainBranch folder does not exist. Skipping backup from MainBranch.')

    # Backup from SillyTavern-DevBranch
    dev_branch = os.path.join(parent_folder, 'SillyTavern-DevBranch\public')
    dev_destination_folder = os.path.join(backup_folder, 'DevBranch', f'{datestamp}_{timestamp}')
    if os.path.exists(dev_branch):
        os.makedirs(dev_destination_folder)
        copy_files(dev_branch, dev_destination_folder, [
            'Backgrounds',
            'Characters',
            'Chats',
            'Groups',
            'Group chats',
            'KoboldAI Settings',
            'NovelAI Settings',
            'OpenAI Settings',
            'TextGen Settings',
            'Themes',
            'User Avatars',
            'Worlds',
            'settings.json'
        ])
    else:
        print('DevBranch folder does not exist. Skipping backup from DevBranch.')

    return 'Backup completed successfully.'


def copy_files(source_dir, destination_dir, directories):
    for directory in directories:
        source_path = os.path.join(source_dir, directory)
        destination_path = os.path.join(destination_dir, directory)
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
        elif os.path.isfile(source_path):
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.copy2(source_path, destination_path)


@app.route('/update-sillytavern', methods=['POST'])
def update_sillytavern():
    branches = request.form.getlist('branch')

    # Get the path of the parent folder

    ParentFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Add the exception for the directory

    subprocess.call(['git', 'update-index', '--skip-worktree', '--ignore-skip-worktree-bits',
                     os.path.join(ParentFolder, 'SillyTavern-MainBranch')])

    output_messages = []

    for folder in branches:

        if folder == 'main':

            if os.path.exists(os.path.join(ParentFolder, 'SillyTavern-MainBranch')):

                output = subprocess.check_output(
                    ['git', '-C', os.path.join(ParentFolder, 'SillyTavern-MainBranch'), 'pull'])

                output_messages.append(output.decode())


            else:

                output_messages.append('Main branch directory does not exist. Skipping update.')




        elif folder == 'dev':

            if os.path.exists(os.path.join(ParentFolder, 'SillyTavern-DevBranch')):

                output = subprocess.check_output(
                    ['git', '-C', os.path.join(ParentFolder, 'SillyTavern-DevBranch'), 'pull'])

                output_messages.append(output.decode())


            else:

                output_messages.append('Dev branch directory does not exist. Skipping update.')




        elif folder == 'extras':

            if os.path.exists(os.path.join(ParentFolder, 'SillyTavern-extras')):

                output = subprocess.check_output(
                    ['git', '-C', os.path.join(ParentFolder, 'SillyTavern-extras'), 'pull'])

                output_messages.append(output.decode())


            else:

                output_messages.append('SillyTavern Extras directory does not exist. Skipping update.')

    return '\n'.join(output_messages)


def load_instances():
    instances_folder = os.path.join(os.path.dirname(__file__), "..", "SillyTavern-Instances")
    instance_names = []

    if os.path.exists(instances_folder):
        instance_names = [name for name in os.listdir(instances_folder) if
                          os.path.isdir(os.path.join(instances_folder, name))]

    return instance_names


@app.route('/profile-manager', methods=['POST', 'GET'])
def profile_manager():
    print("Launching Profile Manager...")
    instances = load_instances()
    return render_template('profile_manager.html', instances=instances)


def copy_instance_files(source, destination):
    dirs_to_copy = [
        "Backgrounds", "Characters", "Chats", "Group chats", "Groups",
        "KoboldAI Settings", "NovelAI Settings", "OpenAI Settings",
        "TextGen Settings", "Themes", "User Avatars", "Worlds"
    ]
    files_to_copy = ["settings.json"]

    for dir_to_copy in dirs_to_copy:
        source_dir = os.path.join(source, dir_to_copy)
        destination_dir = os.path.join(destination, dir_to_copy)

        if os.path.exists(source_dir):
            if os.path.exists(destination_dir):
                shutil.rmtree(destination_dir)
            shutil.copytree(source_dir, destination_dir)

    for file_to_copy in files_to_copy:
        source_file = os.path.join(source, file_to_copy)
        destination_file = os.path.join(destination, file_to_copy)

        if os.path.exists(source_file):
            shutil.copy2(source_file, destination_file)


@app.route('/load-profile', methods=['POST'])
def load_profile():
    data = request.get_json()
    selected_instance = data['instance']
    destination_branch = data['destinationBranch']
    instance_path = os.path.join(os.path.dirname(__file__), "..", "SillyTavern-Instances", selected_instance)

    if destination_branch == 'main':
        destination_path = os.path.join(os.path.dirname(__file__), "..", "SillyTavern-MainBranch", "public")
    else:
        destination_path = os.path.join(os.path.dirname(__file__), "..", "SillyTavern-DevBranch", "public")

    try:
        copy_instance_files(instance_path, destination_path)
        return 'Profile loaded successfully.'
    except Exception as e:
        return str(e), 500


@app.route('/refresh-instances')
def refresh_instances():
    instances = load_instances()
    return jsonify(instances)


@app.route('/save-profile', methods=['POST'])
def save_profile():
    data = request.get_json()
    instance_name = data['instanceName']
    branch_choice = data['branchChoice']

    if branch_choice == 'main':
        destination_branch = "main"
        destination_path = os.path.join(os.path.dirname(__file__), "..", "SillyTavern-MainBranch", "public")
    else:
        destination_branch = "dev"
        destination_path = os.path.join(os.path.dirname(__file__), "..", "SillyTavern-DevBranch", "public")

    new_instance_folder = os.path.join(os.path.dirname(__file__), "..", "SillyTavern-Instances",
                                       instance_name + "-" + destination_branch)

    if os.path.exists(new_instance_folder):
        return "Profile '{}' already exists.".format(instance_name), 400

    try:
        copy_instance_files(destination_path, new_instance_folder)
        return 'Save successful.'
    except Exception as e:
        return str(e), 500


@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    data = request.get_json()
    selected_instance = data['instance']
    instance_folder = os.path.join(os.path.dirname(__file__), "..", "SillyTavern-Instances", selected_instance)

    if os.path.exists(instance_folder):
        try:
            shutil.rmtree(instance_folder)
            return 'Profile deleted successfully.'
        except Exception as e:
            return str(e), 500
    else:
        return 'Profile does not exist.', 400


@app.route('/stem-text', methods=['POST'])
def stem_text():
    try:
        input_text = request.json.get('input_text')
        if not input_text:
            return jsonify({'error': 'Please enter some text.'}), 400

        ps = PorterStemmer()
        stop_words = set(stopwords.words('english'))

        tokens = word_tokenize(input_text)
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words and word not in string.punctuation]
        stemmed_text = " ".join([ps.stem(word) for word in filtered_tokens])

        return jsonify({'stemmed_text': stemmed_text}), 200

    except Exception as e:
        logging.error(f"Error in stem_text function: {e}")
        return jsonify({'error': 'An error occurred.'}), 500


@app.route("/install-stablediffusion", methods=['POST'])
def install_stablediffusion():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    stable_diffusion_dir = os.path.join(root_dir, "StableDiffusion")
    models_dir = os.path.join(stable_diffusion_dir, "models", "Stable-diffusion")
    git_repo = "https://github.com/AUTOMATIC1111/stable-diffusion-webui.git"

    try:
        # Check if the StableDiffusion folder exists
        if not os.path.exists(stable_diffusion_dir):
            # Clone the git repository into the StableDiffusion folder
            os.system(f"git clone {git_repo} {stable_diffusion_dir}")

        # Edit the webui-user.bat file
        webui_user_bat_path = os.path.join(stable_diffusion_dir, "webui-user.bat")
        if os.path.exists(webui_user_bat_path):
            shutil.copy(webui_user_bat_path, webui_user_bat_path + ".backup")  # Create a backup of the original file

            # Open the webui-user.bat file for editing
            with open(webui_user_bat_path, 'w') as file:
                file.write("@echo off\n\n")
                file.write("set PYTHON=\n")
                file.write("set GIT=\n")
                file.write("set VENV_DIR=\n")
                file.write("set COMMANDLINE_ARGS= --api --xformers\n")
                file.write("set XFORMERS_PACKAGE=xformers==0.0.17\n\n")
                file.write("call webui.bat")

        return jsonify({"message": "StableDiffusion and models installed successfully."}), 200

    except Exception as e:
        print(f"An error occurred during installation: {e}")
        return jsonify({"error": f"An error occurred during installation: {e}"}), 500


@app.route("/install-sd-models", methods=['POST'])
def install_sd_models():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    stable_diffusion_dir = os.path.join(root_dir, "StableDiffusion")
    models_dir = os.path.join(stable_diffusion_dir, "models", "Stable-diffusion")
    git_repo = "https://github.com/AUTOMATIC1111/stable-diffusion-webui.git"

    try:
        # Check if the StableDiffusion folder exists
        if not os.path.exists(stable_diffusion_dir):
            return "Please install StableDiffusion First"

        # Get the selected models from the request
        selected_models = request.json.get('models', [])

        # Model IDs and names
        model_info = {
            "model2": {
                "id": 15236,
                "name": "Deliberate"
            },
            "model3": {
                "id": 11745,
                "name": "ChilloutMix"
            },
            "model4": {
                "id": 94640,
                "name": "majicMIX"
            },
            "model5": {
                "id": 94081,
                "name": "DreamShaper"
            },
            "model6": {
                "id": 29460,
                "name": "Realistic Vision"
            },
            "model7": {
                "id": 4007,
                "name": "Protogen"
            },
            "model8": {
                "id": 48423,
                "name": "CoffeeNSFW"
            },
            "model9": {
                "id": 17233,
                "name": "AbyssOrangeMix3"
            },
            "model10": {
                "id": 6878,
                "name": "Corneo's 7th Heaven Mix"
            }
        }

        # Download the selected models
        for model in selected_models:
            if model in model_info:
                model_id = model_info[model]["id"]
                model_name = model_info[model]["name"]
                model_filename = f"{model_name}.safetensors"
                model_path = os.path.join(models_dir, model_filename)
                model_url = f"https://civitai.com/api/download/models/{model_id}"

                # Download the model using requests with tqdm progress bar
                print(f"Downloading model '{model_name}' from: {model_url}")
                response = requests.get(model_url, stream=True, headers={"content-disposition": "attachment"})

                response.raise_for_status()  # Raise an exception if download fails

                with open(model_path, 'wb') as file:
                    total_size = int(response.headers.get('content-length', 0))
                    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

                    for data in response.iter_content(chunk_size=4096):
                        file.write(data)
                        progress_bar.update(len(data))

                    progress_bar.close()

                print(f"Model '{model_name}' saved at: {model_path}")

        # Edit the webui-user.bat file
        webui_user_bat_path = os.path.join(stable_diffusion_dir, "webui-user.bat")
        if os.path.exists(webui_user_bat_path):
            shutil.copy(webui_user_bat_path, webui_user_bat_path + ".backup")  # Create a backup of the original file

            # Open the webui-user.bat file for editing
            with open(webui_user_bat_path, 'w') as file:
                file.write("@echo off\n\n")
                file.write("set PYTHON=\n")
                file.write("set GIT=\n")
                file.write("set VENV_DIR=\n")
                file.write("set COMMANDLINE_ARGS= --api\n\n")
                file.write("call webui.bat")

        return jsonify({"message": "StableDiffusion and models installed successfully."}), 200

    except Exception as e:
        print(f"An error occurred during installation: {e}")
        return jsonify({"error": f"An error occurred during installation: {e}"}), 500


if __name__ == '__main__':
    # host = get_local_ip()
    port = 6969
    # print(host)
    app.run(port=port,debug=True)
