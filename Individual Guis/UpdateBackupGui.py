import tkinter as tk
from subprocess import Popen

def run_script(script):
    process = Popen(script, shell=True)

def create_button(root, text, command):
    button = tk.Button(root, text=text, command=command, bg='#36393f', fg='white', padx=10, pady=5)
    button.pack(pady=5)
    return button

def create_label(root, text):
    label = tk.Label(root, text=text, bg='#36393f', fg='white')
    label.pack()

# Create the main window
root = tk.Tk()
root.title("Script Launcher")
root.configure(bg='#36393f')

# Add a description label at the top
description_label = tk.Label(root, text="Script Launcher - Update and Backup Scripts", bg='#36393f', fg='white', font=("Helvetica", 16, "bold"))
description_label.pack(pady=10)

# Create labels and buttons for each script
scripts = [
    ("Update and Backup Scripts/Backup SillyTavern Files.bat", "Backup SillyTavern Files"),
    ("Update and Backup Scripts/Update SillyTavern.bat", "Update SillyTavern"),
    ("Update and Backup Scripts/Update SillyTavernSimpleLauncher.bat", "Update SillyTavernSimpleLauncher")
]

for script, label_text in scripts:
    label = create_label(root, label_text)
    button = create_button(root, "Run", lambda file=script: run_script(file))

# Start the GUI event loop
root.mainloop()
