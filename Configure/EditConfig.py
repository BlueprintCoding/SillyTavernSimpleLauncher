import tkinter as tk
from tkinter import messagebox
import configparser
import re 
import os
import subprocess

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the configuration file paths
main_branch_config_file = os.path.join(script_dir, "..", "..", "SillyTavern-MainBranch", "config.conf")
dev_branch_config_file = os.path.join(script_dir, "..", "..", "SillyTavern-DevBranch", "config.conf")

# Create the GUI window
window = tk.Tk()
window.title("Configuration Editor")
window.configure(bg="#36393F")  # Set background color to Discord Dark Mode style
# Configure window padding
window.configure(padx="1.5c", pady="1.5c")

# Function to update the configuration file
def update_config():
    # Get the selected branch
    branch = branch_var.get()

    # Set the configuration file path based on the branch selection
    if branch == "Select Branch":
        messagebox.showerror("Error: Select a branch.")
        return
    elif branch == "Main Branch":
        config_file = main_branch_config_file
    elif branch == "Dev Branch":
        config_file = dev_branch_config_file
    else:
        messagebox.showerror("Error", "Invalid branch selection.")
        return

    # Get the new configuration values
    port = port_entry.get()
    whitelist = whitelist_entry.get()
    whitelistMode = whitelist_mode_var.get()
    basicAuthMode = basic_auth_mode_var.get()
    basicAuthUser = basic_auth_username_entry.get() + ":" + basic_auth_password_entry.get()
    disableThumbnails = disable_thumbnails_var.get()
    autorun = autorun_var.get()
    enableExtensions = enable_extensions_var.get()
    listen = listen_var.get()
    allowKeysExposure = allow_keys_exposure_var.get()

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
            updated_content.append(f"const whitelistMode = {str(whitelistMode).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const basicAuthMode"):
            updated_content.append(f"const basicAuthMode = {str(basicAuthMode).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const basicAuthUser"):
            updated_content.append(f"const basicAuthUser = {{username: \"{basicAuthUser.split(':')[0]}\", password: \"{basicAuthUser.split(':')[1]}\"}}; //{line.split('//', 1)[1]}")
        elif line.startswith("const disableThumbnails"):
            updated_content.append(f"const disableThumbnails = {str(disableThumbnails).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const autorun"):
            updated_content.append(f"const autorun = {str(autorun).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const enableExtensions"):
            updated_content.append(f"const enableExtensions = {str(enableExtensions).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const listen"):
            updated_content.append(f"const listen = {str(listen).lower()}; //{line.split('//', 1)[1]}")
        elif line.startswith("const allowKeysExposure"):
            updated_content.append(f"const allowKeysExposure = {str(allowKeysExposure).lower()}; //{line.split('//', 1)[1]}")
        else:
            updated_content.append(line)

    # Write the updated config content to the file
    with open(config_file, "w") as f:
        f.writelines(updated_content)

    messagebox.showinfo("Success", "Configuration file updated successfully.")



# Branch selection change event handler
def branch_selection_change(*args):
    # Load default values when branch selection changes
    load_defaults()

# Branch selection
branch_label = tk.Label(window, text="Select the branch:", bg="#36393F", fg="white")
branch_label.pack()

branch_var = tk.StringVar(window)
branch_var.set("Select Branch...")
branch_var.trace("w", branch_selection_change)  # Bind the branch selection change event
branch_option_menu = tk.OptionMenu(window, branch_var, "Select Branch", "Main Branch", "Dev Branch")
branch_option_menu.config(bg="#36393F", fg="white", activebackground="#7289DA", activeforeground="white")
branch_option_menu.pack()



# Port
port_label = tk.Label(window, text="Port:", bg="#36393F", fg="white")
port_label.pack()

port_entry = tk.Entry(window)
port_entry.pack()

# Whitelist
whitelist_label = tk.Label(window, text="Whitelist:", bg="#36393F", fg="white")
whitelist_label.pack()

whitelist_entry = tk.Entry(window)
whitelist_entry.pack()

# Whitelist Mode
whitelist_mode_var = tk.BooleanVar(window)
whitelist_mode_var.set(True)
whitelist_mode_checkbox = tk.Checkbutton(window, text="Whitelist Mode", variable=whitelist_mode_var, bg="#36393F", fg="white", activebackground="#7289DA", activeforeground="white", selectcolor="#36393F")
whitelist_mode_checkbox.pack()

# Basic Auth Mode
basic_auth_mode_var = tk.BooleanVar(window)
basic_auth_mode_var.set(False)
basic_auth_mode_checkbox = tk.Checkbutton(window, text="Basic Auth Mode", variable=basic_auth_mode_var, bg="#36393F", fg="white", activebackground="#7289DA", activeforeground="white", selectcolor="#36393F")
basic_auth_mode_checkbox.pack()

# Basic Auth User
basic_auth_username_label = tk.Label(window, text="Username:", bg="#36393F", fg="white")
basic_auth_username_label.pack()

basic_auth_username_entry = tk.Entry(window)
basic_auth_username_entry.pack()

basic_auth_password_label = tk.Label(window, text="Password:", bg="#36393F", fg="white")
basic_auth_password_label.pack()

basic_auth_password_entry = tk.Entry(window, show="")
basic_auth_password_entry.pack()

# Disable Thumbnails
disable_thumbnails_var = tk.BooleanVar(window)
disable_thumbnails_var.set(False)
disable_thumbnails_checkbox = tk.Checkbutton(window, text="Disable Thumbnails", variable=disable_thumbnails_var, bg="#36393F", fg="white", activebackground="#7289DA", activeforeground="white", selectcolor="#36393F")
disable_thumbnails_checkbox.pack()

# Autorun
autorun_var = tk.BooleanVar(window)
autorun_var.set(True)
autorun_checkbox = tk.Checkbutton(window, text="Autorun", variable=autorun_var, bg="#36393F", fg="white", activebackground="#7289DA", activeforeground="white", selectcolor="#36393F")
autorun_checkbox.pack()

# Enable Extensions
enable_extensions_var = tk.BooleanVar(window)
enable_extensions_var.set(True)
enable_extensions_checkbox = tk.Checkbutton(window, text="Enable Extensions", variable=enable_extensions_var, bg="#36393F", fg="white", activebackground="#7289DA", activeforeground="white", selectcolor="#36393F")
enable_extensions_checkbox.pack()

# Listen
listen_var = tk.BooleanVar(window)
listen_var.set(True)
listen_checkbox = tk.Checkbutton(window, text="Listen", variable=listen_var, bg="#36393F", fg="white", activebackground="#7289DA", activeforeground="white", selectcolor="#36393F")
listen_checkbox.pack()

# Allow Keys Exposure
allow_keys_exposure_var = tk.BooleanVar(window)
allow_keys_exposure_var.set(False)
allow_keys_exposure_checkbox = tk.Checkbutton(window, text="Allow Keys Exposure", variable=allow_keys_exposure_var, bg="#36393F", fg="white", activebackground="#7289DA", activeforeground="white", selectcolor="#36393F")
allow_keys_exposure_checkbox.pack()

# Load default values from config files
def load_defaults():
    # Get the selected branch
    branch = branch_var.get()

    # Set the configuration file path based on the branch selection
    if branch == "Main Branch":
        config_file = main_branch_config_file
    elif branch == "Dev Branch":
        config_file = dev_branch_config_file
    else:
        messagebox.showerror("Error", "Invalid branch selection.")
        return

    try:
        with open(config_file, "r") as f:
            config_content = f.read()

            # Extract the default values from the config file using regex
            default_values = re.findall(r"const (\w+) = ([^;]+);", config_content, re.MULTILINE)

            # Set the default values in the GUI
            for var_name, var_value in default_values:
                if var_name == "port":
                    port_entry.delete(0, tk.END)
                    port_entry.insert(0, var_value)
                elif var_name == "whitelist":
                    # Remove brackets and single quotes from the string
                    cleaned_value = var_value.strip("['']").replace("', '", " ")
                    whitelist_entry.delete(0, tk.END)
                    whitelist_entry.insert(0, cleaned_value)
                elif var_name == "whitelistMode":
                    whitelist_mode_var.set(var_value)
                elif var_name == "basicAuthMode":
                    basic_auth_mode_var.set(var_value)
                elif var_name == "basicAuthUser":
                    # Extract the username and password values using regular expressions
                    match = re.search(r'username: "([^"]+)"', var_value)
                    if match:
                        username = match.group(1)
                    else:
                        username = ""
                    match = re.search(r'password: "([^"]+)"', var_value)
                    if match:
                        password = match.group(1)
                    else:
                        password = ""
                    basic_auth_username_entry.delete(0, tk.END)
                    basic_auth_username_entry.insert(0, username)
                    basic_auth_password_entry.delete(0, tk.END)
                    basic_auth_password_entry.insert(0, password)
                elif var_name == "disableThumbnails":
                    disable_thumbnails_var.set(var_value)
                elif var_name == "autorun":
                    autorun_var.set(var_value)
                elif var_name == "enableExtensions":
                    enable_extensions_var.set(var_value)
                elif var_name == "listen":
                    listen_var.set(var_value)
                elif var_name == "allowKeysExposure":
                    allow_keys_exposure_var.set(var_value)

        messagebox.showinfo("Success", "Default values loaded successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error loading default values: {str(e)}")


# Load default values on launch
#load_defaults()


# Update button
update_button = tk.Button(window, text="Update Config", command=update_config, bg="#7289DA", fg="white", activebackground="#7289DA", activeforeground="white")
update_button.pack()


# Function to open the config file in the default system text editor
def open_config_file():
    # Get the selected branch
    branch = branch_var.get()
	
	

 # Set the configuration file path based on the branch selection
    if branch == "Select Branch":
        messagebox.showerror("Error: Select a branch.")
    elif branch == "Main Branch":
        config_file = main_branch_config_file
    elif branch == "Dev Branch":
        config_file = dev_branch_config_file
    else:
        messagebox.showerror("Error", "Invalid branch selection.")
        return

    try:
        # Open the config file in the default system text editor
       subprocess.run(["start", config_file], shell=True)

    except Exception as e:
        messagebox.showerror("Error", f"Error opening config file: {str(e)}")

# Open config file button
open_file_button = tk.Button(window, text="Open Config File", command=open_config_file, bg="#7289DA", fg="white", activebackground="#7289DA", activeforeground="white")
open_file_button.pack(side="bottom")

# Run the GUI
window.mainloop()

