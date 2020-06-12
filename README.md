# Script for a single MySQL database sync from a SFTP server

## Requirements

This script was made for Windows Server in mind. You can adapt it to use on Linux or MacOS, should be easy.

Python version 3

Python dependencies:
  - pysftp
  - pymysql

## Usage

First, you should duplicate the <b>env_default.py</b> file and rename it to <b>env.py</b>.
This are the enviorement variables for the current instance. 