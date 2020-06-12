# Script for a single MySQL database sync from a SFTP server

## Requirements

This script was made for Windows Server in mind. You can adapt it to use on Linux or MacOS, should be easy.

Python version 3

Python dependencies:
  - pysftp
  - pymysql

## Usage

- Duplicate the <b>env_default.py</b> file and rename it to <b>env.py</b>.
This are the enviorement variables for the current instance. 

- Complete the variables with your configuration.

- In case you're on Windows, and mysqldump isn't on the PATH, make a direct access to the MySQL installation folder, inside bin folder is mysqldump.exe.

## Troubleshooting