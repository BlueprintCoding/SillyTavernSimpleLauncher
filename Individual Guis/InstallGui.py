import tkinter as tk
import subprocess

def run_batch_file(batch_file):
    process = subprocess.Popen(batch_file, shell=True)
    process.communicate()  # Wait for the process to complete

def create_button(root, text, command):
    button = tk.Button(root, text=text, command=command, bg='#36393f', fg='white', padx=10, pady=5)
    button.pack(pady=5)
    return button

def create_label(root, text):
    label = tk.Label(root, text=text, bg='#36393f', fg='white')
    label.pack()

# Create the main window
root = tk.Tk()
root.title("Batch File Launcher")
root.configure(bg='#36393f')

# Add a description label at the top
description_label = tk.Label(root, text="Click each of these run buttons in order from top to bottom. \n Wait for each command prompt window to finish before clicking the next button", bg='#36393f', fg='white', font=("Helvetica", 14, "bold"))
description_label.pack(pady=10)

# Create labels and buttons for each batch file
batch_files = [
    ("Install Scripts/1 - Install SillyTavern Dependencies - Run 1st.bat", "1 - Install SillyTavern Dependencies - Run 1st"),
    ("Install Scripts/2 - Install SillyTavern Dependencies - Run 2nd.bat", "2 - Install SillyTavern Dependencies - Run 2nd"),
    ("Install Scripts/3a - Install SillyTavern - Main Branch.bat", "3a - Install SillyTavern - Main Branch"),
    ("Install Scripts/3b - Install SillyTavern - Developer Preview Branch.bat", "3b - Install SillyTavern - Developer Preview Branch"),
    ("Install Scripts/4 - Install SillyTavernExtras - Optional.bat", "4 - Install SillyTavernExtras - Optional")
]

for batch_file, label_text in batch_files:
    label = create_label(root, label_text)
    button = create_button(root, "Run", lambda file=batch_file: run_batch_file(file))

# Start the GUI event loop
root.mainloop()
