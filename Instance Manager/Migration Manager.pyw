<!DOCTYPE html>
<html>
<head>
    <title>Silly Tavern Profile Migrator</title>
    <style>
        body {
            background-color: #36393f;
            color: #b5bac1;
            font-family: Arial, sans-serif;
        }

        h1 {
            text-align: center;
        }

        .container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
        }

        input[type="text"],
        select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }

        .btn {
            background-color: #b5bac1;
            color: #313338;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }

        .btn:hover {
            background-color: #a0a5ad;
        }

        .success-msg {
            background-color: #d5f5e3;
            color: #2c3e50;
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 4px;
        }

        .error-msg {
            background-color: #f8d7da;
            color: #721c24;
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 4px;
        }

        .warning-msg {
            background-color: #fff3cd;
            color: #856404;
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>Silly Tavern Profile Migrator</h1>

    <div class="container">
        <form action="#" method="POST" id="migrate-form">
            <div class="form-group">
                <label for="source-directory">Previously Installed SillyTavern Folder:</label>
                <input type="text" name="source_directory" id="source-directory" required>
                <small>Example: C:\SillyTavern</small>
            </div>

            <div class="form-group">
                <label for="new-instance-name">Save a new profile:</label>
                <input type="text" name="new_instance_name" id="new-instance-name" required>
                <small>Enter a name for the new profile</small>
            </div>

            <div class="form-group">
                <label for="branch-choice">Select the branch for the new profile:</label>
                <select name="branch_choice" id="branch-choice">
                    <option value="main">Main Branch</option>
                    <option value="dev">Dev Branch</option>
                </select>
            </div>

            <div class="form-group">
                <button type="submit" class="btn">Save New Profile</button>
            </div>
        </form>

        <div id="message-container"></div>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var migrateForm = document.getElementById("migrate-form");
            var messageContainer = document.getElementById("message-container");

            migrateForm.addEventListener("submit", function(event) {
                event.preventDefault();
                var formData = new FormData(migrateForm);
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "/migrate-instance", true);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            var response = JSON.parse(xhr.responseText);
                            showMessage(response.message, response.type);
                        } else {
                            showMessage("An error occurred during the profile migration.", "error");
                        }
                    }
                };
                xhr.send(formData);
            });

            function showMessage(message, type) {
                var messageElement = document.createElement("div");
                messageElement.textContent = message;
                messageElement.classList.add(type + "-msg");
                messageContainer.appendChild(messageElement);
                setTimeout(function() {
                    messageElement.remove();
                }, 3000);
            }
        });
    </script>
</body>
</html>
