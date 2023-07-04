function waitForServerAlive(port) {
    console.log(port);
    return new Promise((resolve, reject) => {
        const intervalId = setInterval(() => {
            fetch(`http://localhost:${port}`)
                .then(response => {
                    if (response.ok) {
                        console.log("Server is alive.");
                        clearInterval(intervalId);
                        resolve();
                    }
                })
                .catch(error => {
                    console.log("Server is not yet alive.");
                });
        }, 1000);
    });
}

function showLoadingSpinner(message) {
    Swal.fire({
        title: '',
        html: `<div class="swal-spinner"></div><br>${message}`,
        showConfirmButton: false,
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
}


function hideLoadingSpinner() {
    Swal.close();
}

function disableButtons() {
    // Disable all buttonsop
    var buttons = document.getElementsByTagName("button");
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].disabled = true;
    }
}

function enableButtons() {
    // Reload the index page
    location.reload();
}

function launchMain() {
    showLoadingSpinner("Launching ST Main, please wait...");
    let serverLaunched = false;

    fetch('/launch-main', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            if (data.port) {
                console.log("Launching ST Main...");
                waitForServerAlive(data.port)
                    .then(() => {
                        console.log("Server is alive.");
                        serverLaunched = true;
                        hideLoadingSpinner();
                    })
                    .catch(() => {
                        console.error("Server launch timed out.");
                        hideLoadingSpinner();
                        showTimeoutMessage();
                    });
            } else {
                console.error("Failed to launch ST Main.");
                hideLoadingSpinner();
                showTimeoutMessage();
            }
        })
        .catch(error => {
            console.error("An error occurred:", error);
            hideLoadingSpinner();
            showTimeoutMessage();
        });

    // Timeout to hide loading spinner after 15 seconds
    const timeoutId = setTimeout(() => {
        hideLoadingSpinner();
        showTimeoutMessage();
    }, 15000);

    // Function to show timeout message
    function showTimeoutMessage() {
        clearTimeout(timeoutId); // Clear the timeout if the server launch was successful
        if (!serverLaunched) {
            Swal.fire({
                icon: 'info',
                title: 'Launch Timed Out',
                text: 'If SillyTavern launched successfully, you can ignore this message. (If this is the first time launching ST after install it may still be launching) You can check the command prompt to verify',
                confirmButtonText: 'OK'
            });
        }
    }
}


function launchDev() {
    showLoadingSpinner("Launching ST Dev, please wait...");
    let serverLaunched = false;

    fetch('/launch-dev', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            if (data.port) {
                console.log("Launching ST Dev...");
                waitForServerAlive(data.port)
                    .then(() => {
                        console.log("Server is alive.");
                        serverLaunched = true;
                        hideLoadingSpinner();
                    })
                    .catch(() => {
                        console.error("Server launch timed out.");
                        hideLoadingSpinner();
                        showTimeoutMessage();
                    });
            } else {
                console.error("Failed to launch ST Dev.");
                hideLoadingSpinner();
                showTimeoutMessage();
            }
        })
        .catch(error => {
            console.error("An error occurred:", error);
            hideLoadingSpinner();
            showTimeoutMessage();
        });

    // Timeout to hide loading spinner after 20 seconds
    const timeoutId = setTimeout(() => {
        hideLoadingSpinner();
        showTimeoutMessage();
    }, 20000);

    // Function to show timeout message
    function showTimeoutMessage() {
        clearTimeout(timeoutId); // Clear the timeout if the server launch was successful
        if (!serverLaunched) {
            Swal.fire({
                icon: 'info',
                title: 'Launch Timed Out',
                text: 'If SillyTavern launched successfully, you can ignore this message. (If this is the first time launching ST after install it may still be launching) You can check the command prompt to verify',
                confirmButtonText: 'OK'
            });
        }
    }
}


function launchExtras() {
    fetch('/extras-manager', {method: 'GET'})
        .then(response => {
            if (response.ok) {
                console.log("Launching ST Extras...");
                window.location.href = "/extras-manager"; // Redirect to the profile manager page
            } else {
                console.error("Failed to launch ST Extras.");
            }
        })
        .catch(error => {
            console.error("An error occurred:", error);
        });
}

function launchProfileManager() {
    fetch('/profile-manager', {method: 'POST'})
        .then(response => {
            if (response.ok) {
                console.log("Launching Profile Manager...");
                window.location.href = "/profile-manager"; // Redirect to the profile manager page
            } else {
                console.error("Failed to launch Profile Manager.");
            }
        })
        .catch(error => {
            console.error("An error occurred:", error);
        });
}

function editConfig() {
    window.location.href = "/configuration";
}


function closeSillyTavern() {
    fetch("/close-sillytavern", {method: "POST"})
        .then(response => response.text())
        .then(result => {
            console.log(result); // Optional: Print the result in the console
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function shutdownSTSL() {
    showLoadingSpinner("Shutting Down Servers, please wait...");
    fetch('/shutdown-stsl')
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            hideLoadingSpinner();
            let message = 'STSL, SillyTavern, and all other servers have been shut down.\n\nYou can close this window and any open command prompts.\n\n';

            Swal.fire({
                icon: 'success',
                title: 'Shutdown Successful',
                text: message,
                confirmButtonText: 'Close'
            }).then(function () {
                window.close(); // Close the current tab
            });
        })
        .catch(function (error) {
            hideLoadingSpinner();
            let message = 'STSL, SillyTavern, and all other servers have been shut down.\n\nYou can close this window and any open command prompts.\n\n';

            Swal.fire({
                icon: 'success',
                title: 'Shutdown Successful',
                text: message,
                confirmButtonText: 'Close'
            }).then(function () {
                window.close(); // Close the current tab
            });
        });
}


function showLoading() {
    document.getElementById('loadingContainer').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingContainer').style.display = 'none';
}

function install(module) {
    disableButtons();
    showLoading();

    fetch('/install', {method: 'POST', body: module})
        .then(response => response.text())
        .then(message => {
            Swal.fire({
                icon: 'success',
                title: 'Installation Successful',
                text: message,
            }).then(() => {
                hideLoading();
                enableButtons();
            });

        })
        .catch(error => {
            console.error(error);
            Swal.fire({
                icon: 'error',
                title: 'Installation Failed',
                text: 'An error occurred during installation.',
            }).then(() => {
                hideLoading();
                enableButtons();
            });

        });
}


// function enableButton(module) {
//   const button = document.querySelector(`button[data-module="${module}"]`);
//   button.removeAttribute('disabled');
//   button.classList.remove('disabled-button');
// }

function migrateProfile() {
    window.location.href = "/migrate-profile";
}

function backupST() {
    fetch('/backup-sillytavern-files', {method: 'POST'})
        .then(response => {
            if (response.ok) {
                alert('Backup completed successfully.');
            } else {
                alert('Failed to perform backup.');
            }
        })
        .catch(error => {
            console.error('An error occurred:', error);
        });
}

function executeScript(scriptName, branch) {
    if (scriptName === 'Update SillyTavern') {
        fetch('/update-sillytavern', {method: 'POST', body: new URLSearchParams({branch})})
            .then(response => response.text())
            .then(result => {
                alert(result);
            })
            .catch(error => {
                console.error('An error occurred:', error);
            });
    }
}

function showUpdateInstructions(latest_release) {
    var updateInstructions = "To update, close STSL and run the \"Update STSL.bat\" to update automatically or click the \"Releases\" button below to see the latest release notes.";

    Swal.fire({
        title: "Latest Release: " + latest_release,
        html: updateInstructions,
        icon: "info",
        confirmButtonText: "Releases",
        showCloseButton: true,
    }).then((result) => {
        if (result.isConfirmed) {
            window.open("https://github.com/BlueprintCoding/SillyTavernSimpleLauncher/releases", "_blank");
        }
    });
}


function openOptimizePrompt() {
    // Show loading spinner
//this.showLoadingSpinner("Loading Summarization Model...If this is your first time opening this tool it could take a few minutes to download the 3.2GB summary model");
    window.location.href = '/optimize-prompt';
}


function openURL(url) {
    window.open(url, '_blank');
}

function showContent(tabName) {
    // Hide all content divs
    var contentDivs = document.getElementsByClassName("content");
    for (var i = 0; i < contentDivs.length; i++) {
        contentDivs[i].classList.remove("active");
    }

    // Deactivate all tabs
    var tabs = document.getElementsByClassName("tab");
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove("active");
    }

    // Show selected content
    var selectedContent = document.getElementById(tabName);
    if (selectedContent) {
        selectedContent.classList.add("active");
    }

    // Activate selected tab
    var tabButtons = document.getElementsByClassName("tab");
    for (var i = 0; i < tabButtons.length; i++) {
        if (tabButtons[i].getAttribute("onclick") === "showContent('" + tabName + "')") {
            tabButtons[i].classList.add("active");
        }
    }
}
