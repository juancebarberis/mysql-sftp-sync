from env import *
import pysftp
import os
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

def create_database():
  '''
  Create the database if not exists
  '''
  db = pymysql.connect(LOCAL_DB_HOST, LOCAL_DB_USER, LOCAL_DB_PASSWORD)
  cursor = db.cursor()

  drop = cursor.execute("CREATE DATABASE IF NOT EXISTS "+ LOCAL_DB_NAME +";")
  
  db.close()

  
def dump():
  os.system('cmd /k "mysqldump.lnk --add-drop-database '+ LOCAL_DB_NAME +' < out/output.sql"') 


def main():
  get_file()
  create_database()
  dump()

main()