Network Management System

This repository contains a Network Management System (NMS) built with Python, designed to streamline network administration tasks like configuration management, interface monitoring, and backups. The system is tailored for managing routers, switches, and other network devices.
Features

    Device Login and Management: Secure login via SSH for device interaction.
    Backup and Restore: Automated configuration backups and restoration processes.
    Interface Scanning: Scans and retrieves interface details from devices.
    Alert System: Proactively alerts administrators of network issues.
    Templates and Configuration: Customizable templates for device configuration.
    Database Integration: Includes an SQLite database for storing network-related data.

Project Structure

    alert.py: Generates alerts for network issues.
    backupConfig.py: Handles configuration backup tasks.
    junosLogin.py, sshLogin.py: Scripts for logging into Junos-based and SSH-enabled devices.
    routerconf.py, switchconf.py: Configuration scripts for routers and switches.
    scan_script.py: Scans and reports the state of interfaces.
    manage.py: Entry point for Django-based web management.
    db.sqlite3: Database file storing device and network data.
    Templates and Static Files: Front-end elements for the web interface.
    LICENSE: The project is licensed under LICENSE.

Requirements

To set up and run this project, ensure the following dependencies are installed:

    Python 3.8+
    Django Framework
    SQLite3
    Paramiko for SSH management
    ntc-templates for template parsing

Install all required packages using:

pip install -r requirements.txt

Setup and Usage

    Clone the Repository:

git clone https://github.com/arbin0/network-management-system.git
cd network-management-system

Configure Devices:

    Update device details in relevant Python scripts or configuration files.

Run the System:

    python manage.py runserver

    Access the Web Interface: Open a browser and navigate to http://127.0.0.1:8000.

    Scripts:
        Use the Python scripts (e.g., scan_script.py, backupConfig.py) for specific network tasks.

Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.
License

This project is licensed under the MIT License.
Contact

For queries or feedback, please reach out via GitHub issues or contact the repository owner.

Let me know if you'd like to customize this further! ​
​
