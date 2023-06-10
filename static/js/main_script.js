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

        function disableButtons() {
            // Disable all buttonsop
            var buttons = document.getElementsByTagName("button");
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].disabled = true;
            }
        }

        function enableButtons() {
            // Enable all buttons
            var buttons = document.getElementsByTagName("button");
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].disabled = false;
            }
        }

        function launchMain() {
            fetch('/launch-main', {method: 'POST'})
                .then(response => {
                    if (response.ok) {
                        console.log("Launching ST Main...");
                    } else {
                        console.error("Failed to launch ST Main.");
                    }
                })
                .catch(error => {
                    console.error("An error occurred:", error);
                });
        }

        function launchDev() {
            fetch('/launch-dev', {method: 'POST'})
                .then(response => {
                    if (response.ok) {
                        console.log("Launching ST Dev...");
                    } else {
                        console.error("Failed to launch ST Dev.");
                    }
                })
                .catch(error => {
                    console.error("An error occurred:", error);
                });
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
                    alert(message);
                    hideLoading();
                    enableButtons();
                })
                .catch(error => {
                    console.error(error);
                    hideLoading();
                    enableButtons();
                });
        }


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