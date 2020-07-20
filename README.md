# Script for a single MySQL database sync from a SFTP server

This script was made for a very specific use case. It basically connects to an SFTP server, download a SQL file from a specific folder and 'dump' it to a MySQL database.

## Requirements

This script was made for Windows Server in mind. You can adapt it to use on Linux or MacOS, should be easy.

Python version >= 3.

Python dependencies:
  - pysftp
  - pymysql

## Usage

- Duplicate the <b>env_default.py</b> file and rename it to <b>env.py</b>.
This are the enviorement variables for the current instance. 

- Complete the variables with your configuration. It's very important to complete the SYSTEM variable with the OS where the script gonna run [windows|linux].

- In case you're on Windows, and mysql.exe isn't on the PATH, make a direct access to the MySQL installation folder, inside bin folder is mysql.exe.

## Troubleshooting

