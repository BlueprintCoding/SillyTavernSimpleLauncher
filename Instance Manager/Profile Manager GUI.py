import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess

def load_instances():
    instances_folder = os.path.join(os.path.dirname(__file__), "..", "..", "SillyTavern-Instances")
    instance_names = []

    if os.path.exists(instances_folder):
        instance_names = [name for name in os.listdir(instances_folder) if
                          os.path.isdir(os.path.join(instances_folder, name))]

    return instance_names


def refresh_instances():
    instances = load_instances()
    instance_combobox['values'] = instances


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


def select_instance():
    selected_instance = instance_combobox.get()
    if selected_instance:
        destination_branch_var = destination_branch.get()
        if destination_branch_var == 'main':
            branch_name = "Main Branch"
            destination_path = os.path.join(os.path.dirname(__file__), "..", "..", "SillyTavern-MainBranch", "public")
        else:
            branch_name = "Dev Branch"
            destination_path = os.path.join(os.path.dirname(__file__), "..", "..", "SillyTavern-DevBranch", "public")

        confirmation = messagebox.askquestion("Confirmation",
                                              "Are you sure you want to replace {} with {}?"
                                              .format(branch_name, selected_instance))
        if confirmation == 'yes':
            source_path = os.path.join(os.path.dirname(__file__), "..", "..", "SillyTavern-Instances",
                                       selected_instance)

            try:
                copy_instance_files(source_path, destination_path)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            else:
                load_status_label.config(text="Profile loaded successfully.", foreground="green")


def save_new_instance():
    new_instance_name = new_instance_name_entry.get().strip()
    if not new_instance_name:
        messagebox.showwarning("Warning", "Please enter a valid profile name.")
        return

    branch_choice_var = branch_choice.get()
    if branch_choice_var == 'main':
        destination_branch = "main"
        destination_path = os.path.join(os.path.dirname(__file__), "..", "..", "SillyTavern-MainBranch", "public")
    else:
        destination_branch = "dev"
        destination_path = os.path.join(os.path.dirname(__file__), "..", "..", "SillyTavern-DevBranch", "public")

    new_instance_folder = os.path.join(os.path.dirname(__file__), "..", "..", "SillyTavern-Instances",
                                       new_instance_name + "-" + destination_branch)

    if os.path.exists(new_instance_folder):
        messagebox.showwarning("Warning", "Profile '{}' already exists.".format(new_instance_name))
        return

    try:
        copy_instance_files(destination_path, new_instance_folder)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        save_status_label.config(text="Save failed.", foreground="red")
    else:
        messagebox.showinfo("Success", "New profile '{}' created successfully.".format(new_instance_name))
        save_status_label.config(text="Save successful.", foreground="green")
        refresh_instances()


def run_backup_script():
    backup_script_path = os.path.join(os.path.dirname(__file__), "..", "Update and Backup Scripts", "Backup SillyTavern Files.bat")
    subprocess.call(backup_script_path, shell=True)


# Set padding values in pixels (px)
padding_x = 100
padding_y = 100

# Create the main window
root = tk.Tk()
root.title("Silly Tavern Profile Selector")
root.configure(bg="#36393f")  # Set the window background color

# Add padding to the window
root.geometry(f"+{padding_x}+{padding_y}")

# Load instances on window load
instances = load_instances()

# Create a label for backup notice
backup_label = ttk.Label(root, text="This feature is in BETA,\nPlease use the backup function before loading and saving profiles.", background="#36393f", foreground="#b5bac1", justify="center")
backup_label.pack(pady=(0, 10), padx=10)

# Create a button to run the backup script
backup_button = ttk.Button(root, text="Run Backup", command=run_backup_script, style="My.TButton")
backup_button.pack(pady=10)

# Create a separator
ttk.Separator(root, orient="horizontal").pack(fill="x", pady=20)

# Create a label for existing instances
label = ttk.Label(root, text="Select an existing profile to load:", background="#36393f", foreground="#b5bac1")
label.pack(pady=10)

# Create a dropdown menu for existing instances
instance_combobox = ttk.Combobox(root, values=instances)
instance_combobox.pack()

# Create a label for destination branch selection
destination_label = ttk.Label(root, text="What branch do you want to replace?\nPlease note overwriting main branches with dev branches could cause unknown issues", background="#36393f", foreground="#b5bac1",justify="center")
destination_label.pack(pady=(0, 10), padx=10)

# Create a style for the radio buttons
radio_style = ttk.Style()
radio_style.configure("Custom.TRadiobutton", background="#36393f", foreground="#b5bac1")

# Create radio buttons for branch selection
destination_branch = tk.StringVar(value='main')
radio_main_branch = ttk.Radiobutton(root, text="Main Branch", variable=destination_branch, value='main', style="Custom.TRadiobutton")
radio_main_branch.pack()
radio_dev_branch = ttk.Radiobutton(root, text="Dev Branch", variable=destination_branch, value='dev', style="Custom.TRadiobutton")
radio_dev_branch.pack()

# Create a button to select an existing instance
select_button = ttk.Button(root, text="Load Profile", command=select_instance, style="My.TButton")
select_button.pack(pady=10)

# Create a button to refresh the dropdown
refresh_button = ttk.Button(root, text="Refresh Profile List", command=refresh_instances, style="My.TButton")
refresh_button.pack(pady=5)

# Create a label for load status
load_status_label = ttk.Label(root, text="", background="#36393f", foreground="#b5bac1")
load_status_label.pack()

# Create a separator
ttk.Separator(root, orient="horizontal").pack(fill="x", pady=20)

# Create a label for new instance section
new_instance_label = ttk.Label(root, text="Save a new profile:", background="#36393f", foreground="#b5bac1")
new_instance_label.pack(pady=10)

# Create an entry for new instance name
new_instance_name_entry = ttk.Entry(root)
new_instance_name_entry.pack()

# Create a label for branch choice
branch_choice_label = ttk.Label(root, text="Select the branch for the new profile:", background="#36393f", foreground="#b5bac1")
branch_choice_label.pack()

# Create radio buttons for branch choice
branch_choice = tk.StringVar(value='main')
radio_main_choice = ttk.Radiobutton(root, text="Main Branch", variable=branch_choice, value='main', style="Custom.TRadiobutton")
radio_main_choice.pack()
radio_dev_choice = ttk.Radiobutton(root, text="Dev Branch", variable=branch_choice, value='dev', style="Custom.TRadiobutton")
radio_dev_choice.pack()

# Create a button to save a new instance
save_new_instance_button = ttk.Button(root, text="Save New Profile", command=save_new_instance, style="My.TButton")
save_new_instance_button.pack(pady=10)

# Create a label for save status
save_status_label = ttk.Label(root, text="", background="#36393f", foreground="#b5bac1")
save_status_label.pack()

# Set the style for buttons
style = ttk.Style()
style.configure("My.TButton", background='#b5bac1', foreground='#313338', padx=10, pady=5, width=60,
                    font=("Helvetica", 10, "bold"))


# Run the main event loop
root.mainloop()
