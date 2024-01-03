### About this application
This application is basically an entry way in order to manage your own password manager with your own database. This are still quite a few improvements to be made, such as switching to asymmetric encryption and improving performance.

### Requirements

This application requires Python 3.10 or later.
You MUST have a mongodb account in order for this to work. Check out [this link to register](https://account.mongodb.com/account/register)
## Getting Started

This application needs a `.env` file in order to work, make sure you create one and add the following lines (replace **[username]**, **[password]** and **[cluster_url]** with the appropriate information):
```
ENV_URL_PRE = "mongodb+srv://[username]:"
ENV_PASSWORD = "[password]"
ENV_URL_POST = "@[cluster_url]/?retryWrites=true&w=majority"
```

Before running the application, make sure to execute the `libraries.ps1` script to install the required libraries. Follow the steps below:

1. **Install Python:**
   - Ensure that you have Python 3.10 installed for compatibility purposes.

2. **Run Libraries Installation:**
   - Open a terminal or command prompt.
   - Navigate to the root directory of the application.
   - Run the following command to execute the `libraries.ps1` script:
     ```powershell
     .\libraries.ps1
     ```

   This script will install the necessary libraries and dependencies for the application.

   You can now open these files in VSCODE WOWWWW