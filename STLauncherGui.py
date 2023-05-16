import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageSequence
import webbrowser
import subprocess
import sys
import os
import win32api
import win32con
import win32event
import win32process
import atexit
import win32api
import win32con

def simulate_alt_f4():
    # Press the Alt key
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    
    # Press the F4 key
    win32api.keybd_event(win32con.VK_F4, 0, 0, 0)
    
    # Release the F4 key
    win32api.keybd_event(win32con.VK_F4, 0, win32con.KEYEVENTF_KEYUP, 0)
    
    # Release the Alt key
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
    
    
def write_pid_to_file():
    pid = str(os.getpid())
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pid_file = os.path.join(script_dir, "py_pid.txt")
    with open(pid_file, "w") as file:
        file.write(pid)

# Register write_pid_to_file() to be called on program exit
atexit.register(write_pid_to_file)

def open_web_link(link):
    webbrowser.open(link)
	
def open_sillytavern_web():
    webbrowser.open("http://localhost:8000/")
    
def run_script(script):
    process = subprocess.Popen(script, creationflags=subprocess.CREATE_NEW_CONSOLE)
    processes[script] = process

def run_script_admin(script):
    
    info = win32process.CreateProcess(
        None,
        f'cmd /c "{script}"',
        None,
        None,
        0,
        win32process.CREATE_NEW_CONSOLE | win32con.CREATE_NEW_PROCESS_GROUP,
        None,
        None,
        win32process.STARTUPINFO()
    )
    hProcess, hThread, dwProcessId, dwThreadId = info
    win32event.WaitForSingleObject(hProcess, win32event.INFINITE)

def create_button(root, text, command):
    button = tk.Button(root, text=text, command=command, bg='#b5bac1', fg='#313338', padx=10, pady=5)
    return button

def create_label(root, text):
    label = tk.Label(root, text=text, bg='#36393f', fg='white')
    return label
	

# Create the main window
root = tk.Tk()
root.title("SillyTavern Simple Launcher")
root.configure(bg='#36393f')
root.configure(padx=16, pady=16)
root.after(0, write_pid_to_file)

# Dictionary to store the Popen objects
processes = {}

# Add a description label at the top
description_label = tk.Label(root, text="SillyTavern Simple Launcher", bg='#36393f', fg='white', font=("Helvetica", 16, "bold"))
description_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="nw")

# Load the animated GIF
image_path = "Img/STSL-Logo-animated.gif"
image = Image.open(image_path)
frames = [ImageTk.PhotoImage(frame.resize((150, 150))) for frame in ImageSequence.Iterator(image)]

# Create a label widget to display the animated GIF
label2 = tk.Label(root)
label2.place(x=600, y=0)

def update_animation(index):
    frame = frames[index]
    label2.configure(image=frame)
    root.after(3500, update_animation, (index + 1) % len(frames))

update_animation(0)

# Create a frame for the Launch and Close section
launch_frame = tk.LabelFrame(root, text="Launch and Close", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"),borderwidth=4)
launch_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

# Create buttons to launch "Launch ST Main.bat"
launch_main_button = create_button(launch_frame, "Launch ST Main", lambda: run_script("Launch Scripts/Launch ST Main.bat")) 
launch_main_button.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="nw")
launch_main_button.configure(width=20)

# Create a button to launch "Launch ST Dev.bat"
launch_dev_button = create_button(launch_frame, "Launch ST Dev", lambda: run_script("Launch Scripts/Launch ST Dev.bat"))
launch_dev_button.grid(row=0, column=1, padx=5, pady=(5, 0), sticky="nw")
launch_dev_button.configure(width=20)

# Create a button to launch "Launch ST Extras.bat"
launch_extras_button = create_button(launch_frame, "Launch ST Extras", lambda: run_script("Launch Scripts/Launch ST Extras.bat"))
launch_extras_button.grid(row=0, column=2, padx=5, pady=(5, 0), sticky="nw")
launch_extras_button.configure(width=20)

# Create a button to open SillyTavern
open_main_button = create_button(launch_frame, "Open SillyTavern", open_sillytavern_web)
open_main_button.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
open_main_button.configure(width=20)

def open_config_gui():
    subprocess.Popen(["python", "Configure/EditConfig.py"])
	
# Create a button to open SillyTavern config
config_button = create_button(launch_frame, "Edit Config SillyTavern", lambda: run_gui_script("Configure/EditConfig.py"))
config_button.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
config_button.configure(width=20)

# Create a button to close SillyTavern
close_button = create_button(launch_frame, "Close SillyTavern", lambda: run_script("Launch Scripts/Close ST.bat"))
close_button.grid(row=1, column=2, padx=5, pady=5, sticky="nw")
close_button.configure(width=20)

# Add an instructions label
instructions_label = tk.Label(root, text="Instructions: Use the following buttons to install and manage SillyTavern and its dependencies. The install scripts must be run in order, and you must wait for each command prompt to finish before running the next step.", bg='#36393f', fg='white', font=("Helvetica", 11, "bold"), justify="left", wraplength=750)
instructions_label.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="nw")

# Create a frame for the Install section
install_frame = tk.LabelFrame(root, text="Install Scripts", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"),borderwidth=4)
install_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="nw")

# Create labels and buttons for each install script
install_scripts = [
    ("Install Scripts/1 - Install SillyTavern Dependencies - Run 1st.bat", "Install SillyTavern Dependencies"),
    ("Install Scripts/2a - Install SillyTavern - Main Branch.bat", "Install SillyTavern - Main Branch"),
    ("Install Scripts/2b - Install SillyTavern - Developer Preview Branch.bat", "Install SillyTavern - Developer Preview Branch (optional)"),
    ("Install Scripts/3 - Install SillyTavernExtras - Optional.bat", "Install SillyTavernExtras (optional)"),
    ("Install Scripts/Check Dependencies.bat", "Check Dependencies")
]

row = 0
for script, label_text in install_scripts:
    label = create_label(install_frame, label_text)
    label.grid(row=row, column=0, sticky="nw")
    if script in ["Install Scripts/2 - Install SillyTavern Dependencies - Run 2nd.bat"]:
        button = create_button(install_frame, "Run", lambda file=script: run_script_admin(file))
    else:
         button = create_button(install_frame, "Run", lambda file=script: subprocess.Popen(file, creationflags=subprocess.CREATE_NEW_CONSOLE))
    button.grid(row=row, column=1, padx=5, pady=(5, 5), sticky="nw")
    
    # Add a separating line
    separator = ttk.Separator(install_frame, orient="horizontal")
    separator.grid(row=row+1, column=0, columnspan=2, pady=(0, 5), sticky="we")
    
    row += 2

tools_frame = tk.LabelFrame(root, text="Tools", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"),borderwidth=4)
tools_frame.place(x=385, y=267)


# Create labels and buttons for each tool script
tool_scripts = [
    ("Update and Backup Scripts/Backup SillyTavern Files.bat", "Backup SillyTavern Files"),
    ("Update and Backup Scripts/Update SillyTavern.bat", "Update SillyTavern"),
    ("Update and Backup Scripts/Update SillyTavernSimpleLauncher.bat", "Update SillyTavernSimpleLauncher"),
    ("Optimization/OptmizePromptGui.py", "OptimizePrompt GUI"),
]

row = 0
for script, label_text in tool_scripts:
    label = create_label(tools_frame, label_text)
    label.grid(row=row, column=0, sticky="nw")
    if script.endswith(".bat"):
        button = create_button(tools_frame, "Run", lambda file=script: subprocess.Popen(file, creationflags=subprocess.CREATE_NEW_CONSOLE))
    else:
        button = create_button(tools_frame, "Run", lambda file=script: run_script(f'python {file}'))
    button.grid(row=row, column=1, padx=5, pady=(5, 5), sticky="nw")
    
    # Add a separating line
    separator = ttk.Separator(tools_frame, orient="horizontal")
    separator.grid(row=row+1, column=0, columnspan=2, pady=(0, 5), sticky="we")
    
    row += 2


# Create a frame for the Uninstall section
uninstall_frame = tk.LabelFrame(root, text="Uninstall Scripts", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"),borderwidth=4)
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

support_frame = tk.LabelFrame(root, text="Support", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"),borderwidth=4)
support_frame.place(x=225, y=567)


# Create buttons for the web links
button1 = create_button(support_frame, "SillyTavern GitHub", lambda: open_web_link("https://github.com/Cohee1207/SillyTavern"))
button1.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
button1.configure(width=20)

button2 = create_button(support_frame, "STSimpleLauncher GitHub", lambda: open_web_link("https://github.com/blueprintCoding/sillyTavernSimpleLauncher"))
button2.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
button2.configure(width=20)

button3 = create_button(support_frame, "Discord", lambda: open_web_link("https://discord.gg/RZdyAEUPvj"))
button3.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
button3.configure(width=20)

button4 = create_button(support_frame, "Reddit", lambda: open_web_link("https://reddit.com/r/sillyTavernAI/"))
button4.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
button4.configure(width=20)

button5 = create_button(support_frame, "sillytavernai.com", lambda: open_web_link("https://sillytavernai.com"))
button5.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
button5.configure(width=20)

def update_install_paths():
    # Get the parent directory of the GUI file
    parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # List of SillyTavern install directories
    install_directories = [
        "SillyTavern-MainBranch",
        "SillyTavern-DevBranch",
        "SillyTavern-extras",
        "SillyTavern-FileBackups"
    ]

    # Check if each install directory exists
    install_paths_text = ""
    for directory in install_directories:
        path = os.path.join(parent_directory, directory)
        if os.path.exists(path):
            install_paths_text += f"{directory}: {path}\n"
        else:
            install_paths_text += f"{directory}: Not found\n"

    # Update the label with the new install paths
    install_paths_label.configure(text=install_paths_text)

    # Schedule the next update after 10 seconds
    root.after(10000, update_install_paths)


# Create a frame for the Install Paths section
install_paths_frame = tk.LabelFrame(root, text="Install Paths:", bg='#36393f', fg='white', font=("Helvetica", 12, "bold"), borderwidth=4)
install_paths_frame.grid(row=6, column=0, columnspan=1, padx=10, pady=10, sticky="nw")

# Create a label to display the install paths
install_paths_label = create_label(install_paths_frame, "")
install_paths_label.pack()

# Start the initial update
update_install_paths()

# Start the GUI event loop
root.mainloop()

