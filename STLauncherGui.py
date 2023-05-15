import tkinter as tk
from tkinter import ttk
import webbrowser
import subprocess
import sys
import os

def open_web_link(link):
    webbrowser.open(link)

def run_script(script):
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.Popen(script, startupinfo=startup_info, shell=True)

def create_button(root, text, command):
    button = tk.Button(root, text=text, command=command, bg='#36393f', fg='white', padx=10, pady=5)
    return button

def create_label(root, text):
    label = tk.Label(root, text=text, bg='#36393f', fg='white')
    return label

# Create the main window
root = tk.Tk()
root.title("SillyTavernSimpleLauncher")
root.configure(bg='#36393f')
root.configure(padx=16, pady=16)

# Add a description label at the top
description_label = tk.Label(root, text="Silly Tavern Simple Launcher", bg='#36393f', fg='white', font=("Helvetica", 16, "bold"))
description_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="nw")

# Create a frame for the Launch section
launch_frame = tk.LabelFrame(root, text="Launch", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"))
launch_frame.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky="nw")

# Create a button to launch "Launch SillyTavern and Extras.bat"
launch_button = create_button(launch_frame, "Launch SillyTavern and Extras", lambda: run_script("Launch SillyTavern and Extras.bat"))
launch_button.pack(pady=(5, 0), padx=5)

# Create a frame for the Support section
support_frame = tk.LabelFrame(root, text="Support", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"))
support_frame.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky="nw")

# Create buttons for the web links
button1 = create_button(support_frame, "SillyTavern GitHub", lambda: open_web_link("https://github.com/Cohee1207/SillyTavern"))
button1.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

button2 = create_button(support_frame, "SillyTavernSimpleLauncher GitHub", lambda: open_web_link("https://github.com/blueprintCoding/sillyTavernSimpleLauncher"))
button2.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

button3 = create_button(support_frame, "Discord", lambda: open_web_link("https://discord.gg/RZdyAEUPvj"))
button3.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

button4 = create_button(support_frame, "Reddit", lambda: open_web_link("https://reddit.com/r/sillyTavernAI/"))
button4.grid(row=0, column=3, padx=5, pady=5, sticky="nw")

button5 = create_button(support_frame, "sillytavernai.com", lambda: open_web_link("https://sillytavernai.com"))
button5.grid(row=0, column=4, padx=5, pady=5, sticky="nw")

# Add an instructions label
instructions_label = tk.Label(root, text="Instructions: Use the following buttons to install and manage SillyTavern and its dependencies. \nThe install scripts must be run in order, and you must wait for each command prompt to finish before running the next step.", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"), justify="left", wraplength=800)
instructions_label.grid(row=2, column=0, columnspan=5, pady=(10, 0), sticky="nw")

# Create a frame for the Install section
install_frame = tk.LabelFrame(root, text="Install Scripts", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"))
install_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="nw")

# Create labels and buttons for each install script
install_scripts = [
    ("Install Scripts/1 - Install SillyTavern Dependencies - Run 1st.bat", "1 - Install SillyTavern Dependencies - Run 1st"),
    ("Install Scripts/2 - Install SillyTavern Dependencies - Run 2nd.bat", "2 - Install SillyTavern Dependencies - Run 2nd"),
    ("Install Scripts/3a - Install SillyTavern - Main Branch.bat", "3a - Install SillyTavern - Main Branch"),
    ("Install Scripts/3b - Install SillyTavern - Developer Preview Branch.bat", "3b - Install SillyTavern - Developer Preview Branch"),
    ("Install Scripts/4 - Install SillyTavernExtras - Optional.bat", "4 - Install SillyTavernExtras")
]

row = 0
for script, label_text in install_scripts:
    label = create_label(install_frame, label_text)
    label.grid(row=row, column=0, sticky="nw")
    button = create_button(install_frame, "Run", lambda file=script: run_script(file))
    button.grid(row=row, column=1, padx=5, pady=(5, 5), sticky="nw")
    
    # Add a separating line
    separator = ttk.Separator(install_frame, orient="horizontal")
    separator.grid(row=row+1, column=0, columnspan=2, pady=(0, 5), sticky="we")
    
    row += 2

# Create a frame for the Tools section
tools_frame = tk.LabelFrame(root, text="Tools", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"))
tools_frame.grid(row=3, column=1, columnspan=1, padx=10, pady=10, sticky="nw")

# Create labels and buttons for each tool script
tool_scripts = [
    ("Update and Backup Scripts/Backup SillyTavern Files.bat", "Backup SillyTavern Files"),
    ("Update and Backup Scripts/Update SillyTavern.bat", "Update SillyTavern"),
    ("Update and Backup Scripts/Update SillyTavernSimpleLauncher.bat", "Update SillyTavernSimpleLauncher"),
    ("Optimization/OptmizePromptGui.py", "OptimizePrompt GUI")
]

row = 0
for script, label_text in tool_scripts:
    label = create_label(tools_frame, label_text)
    label.grid(row=row, column=0, sticky="nw")
    if script.endswith(".bat"):
        button = create_button(tools_frame, "Run", lambda file=script: run_script(file))
    else:
        button = create_button(tools_frame, "Run", lambda file=script: run_script(f'python {file}'))
    button.grid(row=row, column=1, padx=5, pady=(5, 5), sticky="nw")
    
    # Add a separating line
    separator = ttk.Separator(tools_frame, orient="horizontal")
    separator.grid(row=row+1, column=0, columnspan=2, pady=(0, 5), sticky="we")
    
    row += 2

# Create a frame for the Uninstall section
uninstall_frame = tk.LabelFrame(root, text="Uninstall Scripts", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"))
uninstall_frame.grid(row=4, column=0, columnspan=1, padx=10, pady=10, sticky="nw")

# Create labels and buttons for each uninstall script
uninstall_scripts = [
    ("Uninstall Scripts/Uninstall SillyTavern.bat", "Uninstall SillyTavern"),
    ("Uninstall Scripts/Uninstall SillyTavernExtras.bat", "Uninstall SillyTavernExtras")
]

row = 0
for script, label_text in uninstall_scripts:
    label = create_label(uninstall_frame, label_text)
    label.grid(row=row, column=0, sticky="nw")
    button = create_button(uninstall_frame, "Run", lambda file=script: run_script(file))
    button.grid(row=row, column=1, padx=5, pady=(5, 5), sticky="nw")
    
    # Add a separating line
    separator = ttk.Separator(uninstall_frame, orient="horizontal")
    separator.grid(row=row+1, column=0, columnspan=2, pady=(0, 5), sticky="we")
    
    row += 2

# Create a frame for the Install Paths section
install_paths_frame = tk.LabelFrame(root, text="Install Paths:", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"))
install_paths_frame.grid(row=4, column=1, columnspan=1, pady=10, sticky="nw")

# Read the contents of the InstallPaths.txt file, if it exists
install_paths_file = "InstallPaths.txt"
if os.path.exists(install_paths_file):
    with open(install_paths_file, 'r') as file:
        install_paths = file.read()
    install_paths_text = create_label(install_paths_frame, install_paths)
    install_paths_text.pack()
else:
    install_paths_label = create_label(install_paths_frame, "Install Paths:")
    install_paths_label.pack()
    install_paths_text = create_label(install_paths_frame, "No Install Paths found.")
    install_paths_text.pack()

# Start the GUI event loop
root.mainloop()

