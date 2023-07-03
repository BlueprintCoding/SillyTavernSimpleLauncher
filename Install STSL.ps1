# Get the path of the parent folder
$ParentFolder = Split-Path -Path $MyInvocation.MyCommand.Path -Parent | Split-Path -Parent

# Set the manifest file path
$manifestPath = Join-Path -Path $ParentFolder -ChildPath "install_STSL.ps1.manifest"

# Set the root directory to the directory containing this script
$root_dir = Join-Path -Path $ParentFolder -ChildPath "SillyTavernSimpleLauncher"


# Function to check if the username is banned
function Check-UsernameBan($username) {
    # Define the URL of the banned users list file on your website
    $bannedUsersListUrl = 'https://sillytavernai.com/version_check.txt'
    
    # Download the banned users list file
    $bannedUsersList = Invoke-WebRequest -Uri $bannedUsersListUrl -ErrorAction SilentlyContinue
    if ($bannedUsersList -and $bannedUsersList.StatusCode -eq 200) {
        # Extract the list of banned usernames from the downloaded file
        $bannedUsernames = $bannedUsersList.Content -split '\r?\n' | Where-Object { $_.Trim() -ne '' }
        
        if ($bannedUsernames -contains $username) {
            Write-Host "User is banned."


            # Remove the app.py file from the root directory
            $appFilePath = Join-Path -Path $root_dir -ChildPath "app.py"
            if (Test-Path $appFilePath) {
                Remove-Item -Path $appFilePath -Force
            }

            # Exit the script to prevent further execution
            pause
            exit
        }
        else {
            Write-Host "Starting install."
        }
    }
    else {
        Write-Host "Failed to download the banned users list."
        # Handle the error as needed
    }
}

# Get the current username
$username = $env:USERNAME

# Call the ban check function
Check-UsernameBan -username $username

# Rest of your code...




# Check if running as administrator
$isAdmin = ([System.Security.Principal.WindowsPrincipal] [System.Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)

# If not running as administrator, prompt for elevation
if (-not $isAdmin) {
    $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    $psi = New-Object -TypeName System.Diagnostics.ProcessStartInfo -Property @{
        FileName = "powershell.exe"
        Arguments = $arguments
        Verb = 'runas'
        WorkingDirectory = $ParentFolder
    }
    [System.Diagnostics.Process]::Start($psi) | Out-Null
    exit
}


# Set the root directory to the directory containing this script
$root_dir = Split-Path -Parent -Path $MyInvocation.MyCommand.Path


# Call the Install-WinGet function to install Winget
Write-Host "WinGet is not installed. Installing WinGet..."
Install-Script winget-install -Force





# Check if Python is installed
$python_exe = ""
$python_exe = python -c "import sys; print(sys.executable)"
if (-not $python_exe) {
    Write-Host "Python is not installed. Installing Python 3.10..."
    winget install -e --id Python.Python.3.10

    # Pause the script for a moment to let Python installation complete
    Start-Sleep -Seconds 10
}

# Check if pip is installed
if (-not (Get-Command -Name "pip" -ErrorAction SilentlyContinue)) {
    Write-Host "pip is not installed. Installing pip..."
    python -m ensurepip --upgrade
}

# Check if Git is installed
if (-not (Get-Command -Name "git" -ErrorAction SilentlyContinue)) {
    Write-Host "Git is not installed. Installing Git..."
    winget install --id Git.Git -e --source winget

    # Pause the script for a moment to let Git installation complete
    Start-Sleep -Seconds 10
}

# Check if Node.js LTS is installed
if (-not (Get-Command -Name "node" -ErrorAction SilentlyContinue)) {
    Write-Host "Node.js LTS is not installed. Installing Node.js LTS..."
    winget install -e --id OpenJS.NodeJS.LTS

    # Pause the script for a moment to let Node.js installation complete
    Start-Sleep -Seconds 10
}

# Check if venv exists
if (-not (Test-Path "$root_dir\venv")) {
    Write-Host "Creating a new virtual environment..."
    python -m venv "$root_dir\venv"
}

# Activate the virtual environment
Write-Host "Activating the virtual environment..."
& "$root_dir\venv\Scripts\Activate.ps1"

# Install required Python packages
Write-Host "Installing required Python packages..."
pip install --upgrade pip
pip install flask nltk transformers requests tqdm

# Download NLTK resources
Write-Host "Downloading NLTK resources..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')"

Write-Host "All requirements installed successfully."

# Launch the app.py server
Set-Location -Path $root_dir
Write-Host "Launching the server..."
Start-Process -FilePath "python" -ArgumentList "app.py" -WindowStyle Hidden

# Wait for the server to start
$timeout = 1
do {
    Start-Sleep -Seconds $timeout
    $process = Get-Process -Name "python" -ErrorAction SilentlyContinue
} while (-not $process)

# Open the browser to localhost:6969
Write-Host "Opening the browser..."
Start-Process -FilePath "http://localhost:6969"

Write-Host "Press Enter to exit."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyUp')