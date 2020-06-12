from env import *
import pysftp
from subprocess import check_output
import pymysql

def get_file():
  '''
  Download the SQL file from the remote SFTP server
  '''
  cnopts = pysftp.CnOpts()
  cnopts.hostkeys = None 
  print("")
  with pysftp.Connection(HOST, username=USER, password=PASSWORD, cnopts=cnopts) as sftp:
      print(f"Connection succesfully stablished with {HOST} ({USER})")
      with sftp.cd(DIR):  
          print(f"Actual directory changed to: {DIR}") 
          print(f"Downloading {REMOTE_FILE}")          
          sftp.get(REMOTE_FILE, "out/output.sql")         
          print(f"Download complete.")

def clean_database():
  '''
  Clean the actual mysql database and dump the new
  '''
  db = pymysql.connect(LOCAL_DB_HOST, LOCAL_DB_USER, LOCAL_DB_PASSWORD)
  cursor = db.cursor()

  # Drop the entire database and create new
  drop = cursor.execute("DROP DATABASE "+ LOCAL_DB_NAME +";")
  drop += cursor.execute("CREATE DATABASE IF NOT EXISTS "+ LOCAL_DB_NAME +";")
  
  db.close()

def dump():
  check_output("dir C:", shell=True)


def main():
  get_file()
  clean_database()
  dump()

main()