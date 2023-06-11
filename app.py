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

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and set its level to DEBUG
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the file handler
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

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
    return render_template("index.html")


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
        copy_instance_files(source_directory, new_instance_folder)
        logging.info(f"New profile created: {new_instance_name}-{branch_choice_var}")

        # Return a JSON response indicating success
        return jsonify({"success": True,
                        "message": f"New profile '{new_instance_name}-{branch_choice_var}' created successfully."})

    except Exception as e:
        logging.error(str(e))

        # Return a JSON response indicating error
        return jsonify({"success": False, "message": f"Error creating the new profile: {str(e)}"})


@app.route('/optimize-prompt')
def optimize_prompt():
    return render_template('optimize_prompt.html')


@app.route("/launch-main", methods=['POST'])
def launch_main():
    branch_name = "SillyTavern-MainBranch"
    start_script_dir = os.path.abspath(os.path.join(home_folder, "..", branch_name))
    start_script_path = os.path.join(start_script_dir, "Start.bat")
    subprocess.Popen(start_script_path, shell=True)
    return "Launching ST Main..."


@app.route("/launch-dev", methods=['POST'])
def launch_dev():
    branch_name = "SillyTavern-DevBranch"
    start_script_dir = os.path.abspath(os.path.join(home_folder, "..", branch_name))
    start_script_path = os.path.join(start_script_dir, "Start.bat")
    subprocess.Popen(start_script_path, shell=True)
    return "Launching ST Dev..."


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
    default_values_main = parse_config_file(config_file_path_main)
    default_values_dev = parse_config_file(config_file_path_dev)

    # Pass the default values to the HTML template
    return render_template('edit_config.html', default_values=default_values_main,
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


@app.route("/install-main-branch", methods=['GET', 'POST'])
def install_main_branch():
    parent_folder = os.path.abspath(os.path.join(home_folder, ".."))
    sillytavern_path = os.path.join(parent_folder, "SillyTavern-MainBranch")

    # Check if SillyTavern is already installed
    if os.path.exists(sillytavern_path):
        return "SillyTavern Main is already installed, skipping installation."
    else:
        # Clone SillyTavern repository
        clone_command = ["git", "clone", "https://github.com/SillyTavern/SillyTavern", "-b", "main", sillytavern_path]
        subprocess.Popen(clone_command).wait()
        return "Silly Tavern Main Branch Cloned Successfully."


@app.route("/install-dev-branch", methods=['POST'])
def install_dev_branch():
    parent_folder = os.path.abspath(os.path.join(home_folder, ".."))
    sillytavern_path = os.path.join(parent_folder, "SillyTavern-DevBranch")

    # Check if SillyTavern is already installed
    if os.path.exists(sillytavern_path):
        return "SillyTavern Dev is already installed, skipping installation."
    else:
        # Clone SillyTavern repository
        clone_command = ["git", "clone", "https://github.com/SillyTavern/SillyTavern", "-b", "dev", sillytavern_path]
        subprocess.Popen(clone_command).wait()
        return "Silly Tavern Dev Branch Cloned Successfully."

# Define shared path/directory variables as global
sillytavern_extras_path = None
venv_path = None

@app.route('/extras-manager', methods=['POST', 'GET'])
def extras_manager():
    global sillytavern_extras_path, venv_path

    if request.method == 'POST':
        selected_modules = request.form.getlist('modules')
        custom_flags = request.form.get('custom_flags')

        # Append custom flags to the selected modules if a value is provided
        if custom_flags:
            selected_modules.append(custom_flags)

        launch_extras = True
        start_extras(launch_extras, selected_modules)

        return redirect('/')
    else:
        parent_folder = os.path.abspath(os.path.join(home_folder, ".."))
        sillytavern_extras_path = os.path.join(parent_folder, "SillyTavern-extras")
        venv_path = os.path.join(sillytavern_extras_path, "venv")

        if not os.path.exists(sillytavern_extras_path) or not os.path.exists(venv_path):
            alert_message = "Please install SillyTavern Extras first."
            return render_template('index.html', alert_message=alert_message)

        return render_template('extras_manager.html')


@app.route("/install-extras", methods=['GET', 'POST'])
def install_extras():
    global sillytavern_extras_path, venv_path

    try:
        if not sillytavern_extras_path or not venv_path:
            return jsonify({'error': 'SillyTavern Extras path not found.'}), 500

        if os.path.exists(sillytavern_extras_path):
            logger.info("SillyTavern-extras is already installed. Skipping clone...")
        else:
            subprocess.run(
                ["git", "clone", "https://github.com/SillyTavern/SillyTavern-extras", sillytavern_extras_path])

        venv_path = os.path.join(sillytavern_extras_path, "venv")

        if not os.path.exists(venv_path):
            subprocess.run(["python", "-m", "venv", venv_path])

        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
        subprocess.run([activate_script], shell=True, text=True)

        subprocess.run([os.path.join(venv_path, "Scripts", "python"), "-m", "pip", "install", "--upgrade", "pip"])

        requirements_file = os.path.join(sillytavern_extras_path, "requirements-complete.txt")
        subprocess.run(
            [os.path.join(venv_path, "Scripts", "pip"), "install", "--no-cache-dir", "-r", requirements_file])

        return "SillyTavern-extras Installed..."

    except Exception as e:
        logger.error(f"Error in install_extras function: {e}")
        logger.exception("An error occurred during installation.")

        return jsonify({'error': 'An error occurred during installation.'}), 500


@app.route("/start-extras", methods=['GET', 'POST'])
def start_extras(launch_extras, selected_modules):
    global sillytavern_extras_path, venv_path

    try:
        if not sillytavern_extras_path or not venv_path:
            return jsonify({'error': 'SillyTavern Extras path not found.'}), 500

        if launch_extras:
            enabled_modules_arg = "--enable-modules=" + ",".join(selected_modules)
            sillytavern_extras_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "SillyTavern-extras"))
            activate_venv = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "SillyTavern-extras", "venv", "Scripts", "activate.bat"))
            extras_port = "--port=5100"
            extras_path = os.path.join(sillytavern_extras_path, "server.py")
            venv_path = os.path.join(sillytavern_extras_path, "venv")
            venv_python = os.path.join(venv_path, "Scripts", "python.exe")

            if os.path.exists(venv_python):
                logger.debug("Virtual environment exists.")
            if os.path.exists(extras_path):
                logger.debug("Extras path exists.")

            subprocess.Popen(
                ['start', 'cmd', '/k',
                 f'call {activate_venv} && {venv_python} {extras_path} {enabled_modules_arg} {extras_port}'],
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

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

        return jsonify({'error': 'An error occurred during installation.'}), 500


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

    # Rest of the code
    main_dir = os.path.join(ParentFolder, 'SillyTavern-MainBranch')
    dev_dir = os.path.join(ParentFolder, 'SillyTavern-DevBranch')
    extras_dir = os.path.join(ParentFolder, 'SillyTavern-extras')

    output_messages = []

    for folder in branches:
        if folder == 'main':
            if os.path.exists(main_dir):
                output = subprocess.check_output(['git', '-C', main_dir, 'pull'])
                output_messages.append(output.decode())
            else:
                output_messages.append('Main branch directory does not exist. Skipping update.')

        elif folder == 'dev':
            if os.path.exists(dev_dir):
                output = subprocess.check_output(['git', '-C', dev_dir, 'pull'])
                output_messages.append(output.decode())
            else:
                output_messages.append('Dev branch directory does not exist. Skipping update.')

        elif folder == 'extras':
            if os.path.exists(extras_dir):
                output = subprocess.check_output(['git', '-C', extras_dir, 'pull'])
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


if __name__ == '__main__':
    # host = get_local_ip()
    port = 6969
    # print(host)
    app.run(port=port)
