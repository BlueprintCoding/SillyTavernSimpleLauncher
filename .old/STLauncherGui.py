import tkinter as tk
from tkinter import ttk, messagebox
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
import logging
import urllib.request
import json
import sys

# Check if the script is running inside a virtual environment
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    raise RuntimeError("Please activate the virtual environment before running the script.")


# Configure logging
script_directory = os.path.dirname(os.path.abspath(__file__))
log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs")
os.makedirs(log_directory, exist_ok=True)
log_file_path = os.path.join(log_directory, "MainGuiError.log")
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SillyTavern Simple Launcher")

        try:
            # Check if the SillyTavern main repo directory exists
            repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SillyTavern-MainBranch"))
            if not os.path.exists(repo_dir):
                warning_message = "SillyTavern is not installed"
                logging.warning(warning_message)

            # Check if the STSL-Settings directory exists or create it
            settings_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "STSL-Settings")
            os.makedirs(settings_dir, exist_ok=True)

            # Check if the flags.json file exists or create it with initial value
            flags_file_path = os.path.join(settings_dir, "flags.json")
            if not os.path.exists(flags_file_path):
                flags = {"gui_launch_count": 1}
            else:
                with open(flags_file_path, "r") as file:
                    flags = json.load(file)

            if "gui_launch_count" not in flags:
                flags["gui_launch_count"] = 1
            else:
                flags["gui_launch_count"] += 1

            # Save the updated flags to the JSON file
            with open(flags_file_path, "w") as file:
                json.dump(flags, file)

            # Check if gui_launch_count is 3 or a multiple of 10 and run the profiling function
            if flags["gui_launch_count"] == 3 or flags["gui_launch_count"] % 10 == 0:
                self.run_debugging_profiler()

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
                            padding=[5, 8],
                            justify="center",
                            font=("Helvetica", 10, "bold"))
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

            self.update_label = tk.Label(self.launch_frame, bg="#36393f", fg="white", font=("Helvetica", 12, "bold"))
            self.update_label.grid(row=3, column=0, columnspan=3, pady=10)

            # Check if the repository is updated
            repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SillyTavern-MainBranch"))
            repo_updated, current_version = self.check_repository_updated(repo_dir)

            # Get the latest release tag from the repository
            repo_url = 'https://api.github.com/repos/Cohee1207/SillyTavern'
            latest_release_tag = self.get_latest_release_tag(repo_url)
            new_version = latest_release_tag

            self.show_update_label(repo_updated, current_version, new_version)

        except Exception as e:
            # Log the error and display a generic error message to the user
            logging.exception("An error occurred:")
            messagebox.showerror("Error", "An error occurred. Please check the error log for more details.")

    def run_debugging_profiler(self):
        # Run the DebuggingProfiler.pyw file
        profiling_script = os.path.join("Install Scripts", "DebuggingProfiler.pyw")
        subprocess.Popen(["pythonw", profiling_script])

    def get_latest_release_tag(self, repo_url):
        api_url = f'{repo_url}/releases/latest'
        response = urllib.request.urlopen(api_url)
        data = json.load(response)
        latest_tag = data['tag_name']
        return latest_tag

    def check_repository_updated(self, repo_dir):
        """
        Check if the local Git repository is updated to the current version.
        Returns True if the repository is up to date, False otherwise.
        """

        
        # Initialize current_version to "Not Installed"
        current_version = "Not Installed"
        result = None  # Initialize result variable
        
        # Get the current version number from the local repository's package.json file
        package_file = os.path.join(repo_dir, "package.json")
        try:
            with open(package_file) as f:
                package_data = json.load(f)
                current_version = package_data.get("version", "")
                subprocess.run(["git", "-C", repo_dir, "remote", "update"])
                result = subprocess.run(["git", "-C", repo_dir, "status", "-uno"], capture_output=True, text=True)
        except FileNotFoundError:
            # Handle the FileNotFoundError
            current_version = "Not Installed"        

        if result is not None:  # Check if result is assigned
            return "Your branch is up to date" in result.stdout, current_version
        else:
            return False, current_version

    def show_update_label(self, repo_updated, current_version, new_version):
        """
        Show a label indicating if the repository is updated or not, along with the current and new version numbers.
        """
        if hasattr(self, 'update_label'):
            self.update_label.destroy()  # Destroy the existing label

        # Create a new label with the updated text
        if repo_updated:
            label_text = f"SillyTavern (main) is up to date (Version: {current_version})"
        else:
            if current_version == "Not Installed":
                label_text = f"SillyTavern is not Installed \nGo to the Install Tab."
            else:
                label_text = f"SillyTavern (main) is not up to date\nInstalled Version: {current_version}\nNew Version: {new_version}\nGo to the Tools Tab to update."

        self.update_label = tk.Label(
            self.launch_frame,
            text=label_text,
            bg="#36393f",
            fg="white",
            font=("Helvetica", 12, "bold")
        )
        self.update_label.grid(row=3, column=0, columnspan=3, pady=10)

    def open_web_link(self, link):
        webbrowser.open(link)

    def open_sillytavern_web(self):
        webbrowser.open("http://localhost:8000/")

    def run_script(self, script):
        if script.endswith(".pyw"):
            subprocess.Popen(["pythonw", script], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(script, creationflags=subprocess.CREATE_NEW_CONSOLE)

    # def run_script_admin(self, script):
    #     info = win32process.CreateProcess(
    #         None,
    #         f'cmd /c "{script}"',
    #         None,
    #         None,
    #         0,
    #         win32process.CREATE_NEW_CONSOLE | win32con.CREATE_NEW_PROCESS_GROUP,
    #         None,
    #         None,
    #         win32process.STARTUPINFO()
    #     )
    #     hProcess, hThread, dwProcessId, dwThreadId = info
    #     win32event.WaitForSingleObject(hProcess, win32event.INFINITE)

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

    # def is_admin(self):
    #     try:
    #         return ctypes.windll.shell32.IsUserAnAdmin()
    #     except:
    #         return False

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
            ("Install Scripts/1 - Install SillyTavern Dependencies - Run 1st.bat",
             "Install SillyTavern Dependencies (required)"),
            ("Install Scripts/2a - Install SillyTavern - Main Branch.bat", "Install SillyTavern - Main Branch"),
            ("Install Scripts/2b - Install SillyTavern - Developer Preview Branch.bat",
             "Install SillyTavern - Developer Preview Branch (optional)"),
            ("Instance Manager/Migration Manager.pyw", "Migrate Existing SillyTavern Install as Profile"),
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
        launch_frame.grid(sticky="nsew")  # Use grid instead of pack
        
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SillyTavern-MainBranch"))
        if not os.path.exists(repo_dir):
            warning_message = "SillyTavern is not installed"
            logging.warning(warning_message)
        else:
            repo_updated, current_version = self.check_repository_updated(repo_dir)
            # Get the new version number from the remote repository's tags
            # Replace 'origin' with the appropriate remote name if needed
            subprocess.run(["git", "-C", repo_dir, "fetch", "--tags"])
            result = subprocess.run(["git", "-C", repo_dir, "describe", "--tags", "--abbrev=0"], capture_output=True,
                                text=True)
            new_version = result.stdout.strip()

            self.show_update_label(repo_updated, current_version, new_version)

        # Create buttons to launch "Launch ST Main.bat"
        launch_main_button = self.create_button(launch_frame, "Launch ST Main",
                                                lambda: self.run_start_script("SillyTavern-MainBranch"))
        launch_dev_button = self.create_button(launch_frame, "Launch ST Dev",
                                               lambda: self.run_start_script("SillyTavern-DevBranch"))
        launch_extras_button = self.create_button(launch_frame, "Launch ST Extras",
                                                  lambda: self.run_script("Launch Scripts/Launch ST Extras.bat"))
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
        config_button.grid(row=1, column=0, padx=5, pady=5)
        close_button.grid(row=1, column=1, padx=5, pady=5)
        instance_button = self.create_button(launch_frame, "Change SillyTavern Profile", lambda: open_profile_gui())
        instance_button.grid(row=1, column=2, padx=5, pady=5)

        # Create a separate frame for instance button and label
        instance_frame = ttk.Frame(launch_frame, style="Dark.TFrame")
        instance_frame.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

        # Add a label below the button
        label_text = "^\nThis tool will allow you to save and load different profiles into your main or dev ST instances."
        label = self.create_label(instance_frame, label_text)
        label.config(bg='#36393f', fg='white', justify="center", wraplength=165)
        label.grid(row=0, column=0, padx=10, pady=(0, 5))

        # Create a label to show the update status
        self.update_label = tk.Label(
            launch_frame,
            text="",
            bg="#36393f",
            fg="white",
            font=("Helvetica", 12, "bold")
        )
        self.update_label.grid(row=3, column=0, columnspan=3, pady=10)

        def open_profile_gui():
            subprocess.Popen(["python", "Instance Manager/Profile Manager GUI.pyw"])

        def open_config_gui():
            subprocess.Popen(["python", "Configure/EditConfig.py"])

        # Configure the launch frame to expand with the window
        launch_frame.grid(sticky="nsew")

        # Set the weights of rows and columns to 0 for the instance_frame
        launch_frame.grid_rowconfigure(2, weight=0)
        launch_frame.grid_columnconfigure(1, weight=0)

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
            ("Update and Backup Scripts/Backup SillyTavern Files.bat", "Backup SillyTavern Files\public"),
            ("Update and Backup Scripts/Update SillyTavern.bat", "Update SillyTavern"),
            ("Update and Backup Scripts/Update SillyTavernSimpleLauncher.bat", "Update SillyTavernSimpleLauncher"),
            ("Optimization/OptimizePromptGui.pyw", "OptimizePrompt GUI"),
        ]

        button_width = 60  # Set the desired button width

        for script, label_text in tool_scripts:
            if script.endswith(".pyw"):
                button = self.create_button(tools_frame, label_text,
                                            lambda script=script: self.run_script_in_virtualenv(script))
            else:
                button = self.create_button(tools_frame, label_text, lambda file=script: subprocess.Popen(file,
                                                                                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
            button.config(width=button_width)  # Override the button width
            button.pack(padx=10, pady=(10, 5), anchor="center")

    def run_script_in_virtualenv(self, script):
        virtualenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "venv"))
        pythonw_path = os.path.join(virtualenv_path, "Scripts", "pythonw.exe")
        subprocess.Popen([pythonw_path, script])

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

        button_width = 60  # Set the desired button width

        for script, label_text in uninstall_scripts:
            button = self.create_button(self.uninstall_frame, label_text,
                                        lambda file=script: subprocess.Popen(f'"{file}"', shell=True))
            button.config(width=button_width)  # Override the button width
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
        window_height = 650
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
        # Log the error and display a generic error message to the user
        logging.exception("An error occurred:")
        messagebox.showerror("Error", "An error occurred. Please check the error log for more details.")
