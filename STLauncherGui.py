import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageSequence
import webbrowser
import subprocess
import sys
import os
import win32con
import win32event
import win32process
import win32api
import win32con
import ctypes
import traceback


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SillyTavern Simple Launcher")

        # Create the label frame
        label_frame = tk.Frame(self.root, bg="#1e2124")
        label_frame.pack(fill=tk.X)

        # Load the animated GIF
        image_path = "Img/STSL-Logo-animated.gif"
        image = Image.open(image_path)
        frames = [ImageTk.PhotoImage(frame.resize((150, 150))) for frame in ImageSequence.Iterator(image)]

        # Create a label to display the animated GIF
        label2 = tk.Label(label_frame, image=frames[0], bg="#1e2124")
        label2.pack()

        # Function to update the animation
        def update_animation(index):
            frame = frames[index]
            label2.configure(image=frame)
            root.after(3500, update_animation, (index + 1) % len(frames))

        # Start the animation
        update_animation(0)

        # Create the label
        label = tk.Label(label_frame, text="SillyTavern Simple Launcher", fg="white", bg="#1e2124", font=("Helvetica", 16, "bold"))
        label.pack(padx=10, pady=5)

        # Configure the style for the notebook and tabs
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab",
                        background="#36393e",
                        foreground="white",
                        lightcolor="#2E3C42",
                        borderwidth=0,
                        padding = [5, 8],
                        justify ="center",
                        font = ("Helvetica", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", "#7289da")],
                  foreground=[("selected", "white")])
        style.configure("Dark.TNotebook.Tab", width=150)

        # Set up the notebook widget
        self.notebook = ttk.Notebook(self.root, style="Dark.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_changed)

        # Create the notebook frames
        self.install_frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.launch_frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.tools_frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.uninstall_frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.support_frame = ttk.Frame(self.notebook, style="Dark.TFrame")

        # Add the notebook frames
        self.notebook.add(self.launch_frame, text="Launch")
        self.notebook.add(self.install_frame, text="Install")
        self.notebook.add(self.tools_frame, text="Tools")
        self.notebook.add(self.uninstall_frame, text="Uninstall")
        self.notebook.add(self.support_frame, text="Support")

        # Set up the widgets for each frame
        self.setup_install_frame()
        self.setup_launch_frame()
        self.setup_tools_frame()
        self.setup_uninstall_frame()
        self.setup_support_frame()

    def open_web_link(self, link):
        webbrowser.open(link)

    def open_sillytavern_web(self):
        webbrowser.open("http://localhost:8000/")

    def run_script(self, script):
        process = subprocess.Popen(script, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def run_script_admin(self, script):
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

    def create_button(self, root, text, command):
        button = tk.Button(
            root,
            text=text,
            command=command,
            bg='#b5bac1',
            fg='#313338',
            padx=10,
            pady=5,
            width=20,
            font=("Helvetica", 10, "bold")
        )
        return button

    def create_label(self, root, text):
        label = tk.Label(root, text=text, bg='#36393f', fg='white')
        return label

    def run_start_script(self, branch_name):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if branch_name == "SillyTavern-MainBranch" or branch_name == "SillyTavern-DevBranch":
            start_script_dir = os.path.abspath(os.path.join(script_dir, "..", branch_name))
            start_script_path = os.path.join(start_script_dir, "Start.bat")
            subprocess.Popen(start_script_path, shell=True)
        else:
            print("Invalid branch_name.")

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def stop_node_servers(self):
        if sys.platform == 'win32':
            # Start a new command shell with administrative privileges
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(
                'cmd /c "taskkill /f /im node.exe"',
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                startupinfo=startupinfo
            )
        else:
            print("Stopping Node servers is only supported on Windows.")

        print("Node servers for SillyTavern have been shut down.")

    def setup_install_frame(self):
        # Create the instructions label
        instructions_label = tk.Label(
            self.install_frame,
            text="Instructions: Use the following buttons to install and manage SillyTavern and its dependencies. The Install SillyTavern Dependencies must be run first, and you must wait for each command prompt to finish before running the next step. \nThe 'Install SillyTavern Dependencies' button will close the GUI to activate all the dependencies correctly.",
            bg='#36393f',
            fg='white',
            font=("Helvetica", 11, "bold"),
            justify="center",
            wraplength=500
        )
        instructions_label.pack(padx=10, pady=(10, 5), anchor="center")

        def update_wraplength(event):
            frame_width = event.width
            new_wraplength = frame_width - 20  # Adjust the padding if needed
            instructions_label.config(wraplength=new_wraplength)

        self.install_frame.bind("<Configure>", update_wraplength)

        # Create buttons for each install script
        install_scripts = [
            ("Install Scripts/1 - Install SillyTavern Dependencies - Run 1st.bat", "Install SillyTavern Dependencies (required)"),
            ("Install Scripts/2a - Install SillyTavern - Main Branch.bat", "Install SillyTavern - Main Branch"),
            ("Install Scripts/2b - Install SillyTavern - Developer Preview Branch.bat",
             "Install SillyTavern - Developer Preview Branch (optional)"),
            ("Install Scripts/3 - Install SillyTavernExtras - Optional.bat", "Install SillyTavernExtras (optional)"),
            ("Install Scripts/Check Dependencies.bat", "Check Dependencies")
        ]

        for script, label_text in install_scripts:
            if label_text == "Install SillyTavern Dependencies (required)":
                button = ttk.Button(
                    self.install_frame,
                    text=label_text,
                    command=lambda file=script: self.run_script_and_close_gui(file),
                    style="Dark.TButton"
                )
            else:
                button = ttk.Button(
                    self.install_frame,
                    text=label_text,
                    command=lambda file=script: self.run_script(file),
                    style="Dark.TButton"
                )
            button.pack(padx=10, pady=(5, 10), anchor="w")

            # Center the button text horizontally and vertically
            button.pack_configure(anchor="center")

    def run_script_and_close_gui(self, script):
        # Close the Python GUI
        self.root.destroy()

        # Run the install script
        self.run_script(script)

    def setup_launch_frame(self):
        # Create a new frame for the buttons
        launch_frame = ttk.Frame(self.launch_frame, style="Dark.TFrame")
        launch_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        # Create buttons to launch "Launch ST Main.bat"
        launch_main_button = self.create_button(launch_frame, "Launch ST Main",
                                                lambda: self.run_start_script("SillyTavern-MainBranch"))
        launch_dev_button = self.create_button(launch_frame, "Launch ST Dev",
                                               lambda: self.run_start_script("SillyTavern-DevBranch"))
        launch_extras_button = self.create_button(launch_frame, "Launch ST Extras",
                                                  lambda: self.run_script("Launch Scripts/Launch ST Extras.bat"))
        #open_main_button = self.create_button(launch_frame, "Open SillyTavern", self.open_sillytavern_web)
        config_button = self.create_button(launch_frame, "Edit Config", lambda: open_config_gui())
        close_button = self.create_button(launch_frame, "Close SillyTavern", lambda: self.stop_node_servers())

        # Configure the number of columns and rows in the launch frame
        launch_frame.grid_columnconfigure(0, weight=1)
        launch_frame.grid_columnconfigure(1, weight=1)
        launch_frame.grid_columnconfigure(2, weight=1)
        launch_frame.grid_columnconfigure(3, weight=1)
        launch_frame.grid_columnconfigure(4, weight=1)
        launch_frame.grid_columnconfigure(5, weight=1)

        # Place the buttons using the grid layout
        launch_main_button.grid(row=0, column=0, padx=5, pady=(5, 0))
        launch_dev_button.grid(row=0, column=1, padx=5, pady=(5, 0))
        launch_extras_button.grid(row=0, column=2, padx=5, pady=(5, 0))
        #open_main_button.grid(row=1, column=0, padx=5, pady=5)
        config_button.grid(row=1, column=0, padx=5, pady=5)
        close_button.grid(row=1, column=1, padx=5, pady=5)
        instance_button = self.create_button(launch_frame, "Change SillyTavern Profile", lambda: open_profile_gui())
        instance_button.grid(row=1, column=2, padx=5, pady=5)

        # Create a separate frame for instance button and label
        instance_frame = ttk.Frame(launch_frame, style="Dark.TFrame")
        instance_frame.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        # Add a label below the button
        label_text = "^\nThis tool while allow you to save and load different profiles into your main or dev ST instances."
        label = self.create_label(instance_frame, label_text)
        label.config(bg='#36393f', fg='white', justify="center", wraplength=165)
        label.pack(padx=10, pady=(0, 5))


        def open_profile_gui():
            subprocess.Popen(["python", "Instance Manager/Profile Manager GUI.py"])

        def open_config_gui():
            subprocess.Popen(["python", "Configure/EditConfig.py"])

        # Configure the launch frame to expand with the window
        launch_frame.grid(sticky="nsew")

        # Set the weights of rows and columns to 0 for the instance_frame
        launch_frame.grid_rowconfigure(2, weight=0)
        launch_frame.grid_columnconfigure(1, weight=0)

        def open_profile_gui():
            subprocess.Popen(["python", "Instance Manager/Profile Manager GUI.py"])

        def open_config_gui():
            subprocess.Popen(["python", "Configure/EditConfig.py"])

        # Configure the launch frame to expand with the window
        launch_frame.grid(sticky="nsew")

    def setup_tools_frame(self):
        # Create the label at the top of the frame
        label_text = "Tools"
        label = self.create_label(self.tools_frame, label_text)
        label.config(
            bg='#36393f',
            fg='white',
            font=("Helvetica", 11, "bold"),
            justify="center",
            wraplength=500
        )
        label.pack(padx=10, pady=10, anchor="center")
        # Create a new frame for the buttons
        tools_frame = ttk.Frame(self.tools_frame, style="Dark.TFrame")
        tools_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        # Create widgets for Tools Frame
        tool_scripts = [
            ("Update and Backup Scripts/Backup SillyTavern Files.bat", "Backup SillyTavern Files"),
            ("Update and Backup Scripts/Update SillyTavern.bat", "Update SillyTavern"),
            ("Update and Backup Scripts/Update SillyTavernSimpleLauncher.bat", "Update SillyTavernSimpleLauncher"),
            ("Optimization/OptmizePromptGui.py", "OptimizePrompt GUI"),
        ]

        for script, label_text in tool_scripts:
            if script.endswith(".bat"):
                button = tk.Button(
                    self.tools_frame,
                    text=label_text,
                    command=lambda file=script: subprocess.Popen(file, creationflags=subprocess.CREATE_NEW_CONSOLE),
                    bg='#b5bac1',
                    fg='#313338',
                    padx=10,
                    pady=5,
                    width=60,
                    font=("Helvetica", 10, "bold")
                )
            else:
                button = tk.Button(
                    self.tools_frame,
                    text=label_text,
                    command=lambda file=script: self.run_script(f'python {file}'),
                    bg='#b5bac1',
                    fg='#313338',
                    padx=10,
                    pady=5,
                    width=60,
                    font=("Helvetica", 10, "bold")
                )

            button.pack(padx=10, pady=(10, 5), anchor="center")

    def setup_uninstall_frame(self):
        # Create the label at the top of the frame
        label_text = "Uninstall"
        label = self.create_label(self.uninstall_frame, label_text)
        label.config(
            bg='#36393f',
            fg='white',
            font=("Helvetica", 11, "bold"),
            justify="center",
            wraplength=500
        )
        label.pack(padx=10, pady=10, anchor="center")

        # Create buttons for each uninstall script
        uninstall_scripts = [
            ("Uninstall Scripts/Uninstall SillyTavern.bat", "Uninstall SillyTavern"),
            ("Uninstall Scripts/Uninstall SillyTavernExtras.bat", "Uninstall SillyTavernExtras")
        ]

        for script, label_text in uninstall_scripts:
            if script.endswith(".bat"):
                button = tk.Button(
                    self.uninstall_frame,
                    text=label_text,
                    command=lambda file=script: subprocess.Popen(f'"{file}"', shell=True),
                    bg='#b5bac1',
                    fg='#313338',
                    padx=10,
                    pady=5,
                    width=60,
                    font=("Helvetica", 10, "bold")
                )

            button.pack(padx=10, pady=(10, 5), anchor="center")

    def setup_support_frame(self):
        # Create the label at the top of the frame
        label_text = "Support"
        label = self.create_label(self.support_frame, label_text)
        label.config(
            bg='#36393f',
            fg='white',
            font=("Helvetica", 11, "bold"),
            justify="center",
            wraplength=500
        )
        label.pack(padx=10, pady=10, anchor="center")

        # Create a new frame for the buttons
        support_inner_frame = ttk.Frame(self.support_frame, style="Dark.TFrame")
        support_inner_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        # Create buttons for the web links
        buttons_data = [
            ("SillyTavern GitHub", "https://github.com/Cohee1207/SillyTavern"),
            ("STSimpleLauncher GitHub", "https://github.com/blueprintCoding/sillyTavernSimpleLauncher"),
            ("Discord", "https://discord.gg/RZdyAEUPvj"),
            ("Reddit", "https://reddit.com/r/sillyTavernAI/"),
            ("sillytavernai.com", "https://sillytavernai.com")
        ]

        for label_text, link in buttons_data:
            button = tk.Button(
                support_inner_frame,
                text=label_text,
                command=lambda link=link: self.open_web_link(link),
                bg='#b5bac1',
                fg='#313338',
                padx=10,
                pady=5,
                width=60,
                font=("Helvetica", 10, "bold")
            )
            button.pack(fill=tk.X, padx=5, pady=5)

        # Configure the support inner frame to expand vertically
        support_inner_frame.pack(fill=tk.BOTH, expand=True)

    def tab_changed(self, event):
        # Adjust the notebook frame size to fit the window
        self.notebook.update_idletasks()
        self.notebook_width = self.notebook.winfo_width()
        self.notebook_height = self.notebook.winfo_height()

        # Get the maximum width among all the frames
        max_frame_width = max(
            self.install_frame.winfo_width(),
            self.launch_frame.winfo_width(),
            self.tools_frame.winfo_width(),
            self.uninstall_frame.winfo_width(),
            self.support_frame.winfo_width()
        )

        # Set the window width to the maximum frame width
        self.root.geometry(f"{max_frame_width}x600")

        # Configure the frames to fill the available space
        self.install_frame.config(width=self.notebook_width, height=self.notebook_height)
        self.launch_frame.config(width=self.notebook_width, height=self.notebook_height)
        self.tools_frame.config(width=self.notebook_width, height=self.notebook_height)
        self.uninstall_frame.config(width=self.notebook_width, height=self.notebook_height)
        self.support_frame.config(width=self.notebook_width, height=self.notebook_height)


if __name__ == "__main__":
    try:
        root = tk.Tk()

        # Configure the root window to expand with the user's resolution
        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the window position
        window_width = 600
        window_height = 600
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

        # Configure the root window to expand with the user's resolution
        root.minsize(window_width, window_height)
        root.minsize(window_width, window_height)

        # Set the style for the notebook and frames
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TNotebook", background="#36393f")
        style.configure("Dark.TFrame", background="#36393f")
        style.configure("Dark.TopFrame", background="#1e2124")
        style.configure("Dark.TLabel", background="#36393f", foreground="white")
        style.configure(
            "Dark.TButton",
            background='#b5bac1',
            foreground='#313338',
            padx=10,
            pady=5,
            width=70,
            font=("Helvetica", 10, "bold")
        )

        gui = GUI(root)
        root.mainloop()
    except Exception as e:
        # Log the error traceback
        traceback.print_exc()

        # You can also save the traceback to a log file
        with open("error-gui.log", "w") as f:
            traceback.print_exc(file=f)
