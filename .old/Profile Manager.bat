import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def load_instances():
    instances_folder = os.path.join(os.path.dirname(__file__), "..", "..", "SillyTavern-Instances")
    instance_names = []

    if os.path.exists(instances_folder):
        instance_names = [name for name in os.listdir(instances_folder) if os.path.isdir(os.path.join(instances_folder, name))]

    return instance_names

def refresh_instances():
    instances = load_instances()
    instance_combobox['values'] = instances

def copy_instance_files(source, destination):
    dirs_to_override = [
        "Backgrounds", "Characters", "Chats", "Group chats", "Groups",
        "KoboldAI Settings", "NovelAI Settings", "OpenAI Settings",
        "TextGen Settings", "Themes", "User Avatars", "Worlds"
    ]
    files_to_override = ["settings.json"]

    for dir_to_override in dirs_to_override:
        source_dir = os.path.join(source, dir_to_override)
        destination_dir = os.path.join(destination, dir_to_override)

        if os.path.exists(destination_dir):
            shutil.rmtree(destination_dir)

        shutil.copytree(source_dir, destination_dir)

    for file_to_override in files_to_override:
        source_file = os.path.join(source, file_to_override)
        destination_file = os.path.join(destination, file_to_override)

        if os.path.exists(destination_file):
            os.remove(destination_file)

        shutil.copy2(source_file, destination_file)

def create_instance():
    instance_name = new_instance_entry.get().strip()

    if not instance_name:
        messagebox.showerror("Error", "Please enter a valid instance name.")
        return

    instances_folder = os.path.join(os.path.dirname(__file__), "..", "..", "SillyTavern-Instances")
    destination_folder = os.path.join(instances_folder, instance_name)

    if os.path.exists(destination_folder):
        messagebox.showerror("Error", "Instance '{}' already exists.".format(instance_name))
        return

    try:
        os.mkdir(destination_folder)
        copy_instance_files(new_instance_source, destination_folder)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    messagebox.showinfo("Success", "Instance '{}' created successfully.".format(instance_name))
    refresh_instances()

    new_instance_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Silly Tavern Instance Selector")

# Load instances on window load
instances = load_instances()

# Create a label
label = ttk.Label(root, text="Select an instance:")
label.pack(pady=10)

# Create a dropdown menu
instance_combobox = ttk.Combobox(root, values=instances)
instance_combobox.pack()

# Create a button to select the instance
select_button = ttk.Button(root, text="Select", command=select_instance)
select_button.pack(pady=10)

# Create a button to refresh the dropdown
refresh_button = ttk.Button(root, text="Refresh", command=refresh_instances)
refresh_button.pack(pady=5)

# Create a separator
separator = ttk.Separator(root, orient=tk.HORIZONTAL)
separator.pack(fill=tk.X, pady=10)

# Create a section to save a new instance
new_instance_label = ttk.Label(root, text="Create a new instance:")
new_instance_label.pack(pady=5)

new_instance_frame = ttk.Frame(root)
new_instance_frame.pack()

new_instance_label_source = ttk.Label(new_instance_frame, text="Source:")
new_instance_label_source.grid
