from env import *
import pysftp
import os
import pymysql.cursors

def get_file():
  '''
  Download the SQL file from the remote SFTP server
  '''
  print("")
  cnopts = pysftp.CnOpts()
  cnopts.hostkeys = None 
  with pysftp.Connection(HOST, username=USER, password=PASSWORD, cnopts=cnopts) as sftp:
      print(f"Connection succesfully stablished with {HOST} ({USER})")
      with sftp.cd(DIR):  
          print(f"Actual directory changed to: {DIR}") 
          print(f"Downloading {REMOTE_FILE}")          
          sftp.get(REMOTE_FILE, "out/output.sql")         
          print(f"Download complete.")

def reload_database():
  '''
  Create the database if not exists
  '''
  print("")
  db = pymysql.connect(LOCAL_DB_HOST, LOCAL_DB_USER, LOCAL_DB_PASSWORD)
  cursor = db.cursor()
  cursor.execute("USE information_schema")
  cursor.execute('SELECT COUNT(*) FROM schemata WHERE SCHEMA_NAME=%s', (LOCAL_DB_NAME))
  result = cursor.fetchone()
  
  if(result[0] >= 1):
    print("The database exists.\nExecuting DROP DATABASE...")
    cursor.execute("DROP DATABASE "+ LOCAL_DB_NAME +";")
  else:
    print("The database does not exists. Trying to create...")

  cursor.execute("CREATE DATABASE "+ LOCAL_DB_NAME)
  print(f"Database {LOCAL_DB_NAME} created")
  
  db.close()

  
def dump():
  # Remove .lnk y you're Windows terminal recognize it in a different way.
  print("")
  os.system('cmd /k "mysqldump.lnk --add-drop-database '+ LOCAL_DB_NAME +' < out/output.sql"') 


def main():
  get_file()
  reload_database()
  dump()

main()