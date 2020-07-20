from env import *
import pysftp
from datetime import datetime
import os
import pymysql.cursors
import logging


def get_file():
  '''
  Download the SQL file from the remote SFTP server
  '''
  logging.info("Trying to download from the SFTP server")
  try:
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    cnopts.timeout = 30

    with pysftp.Connection(HOST, username=USER, password=PASSWORD, cnopts=cnopts) as sftp:
        logging.info("Connection succesfully stablished with the SFTP server")
        with sftp.cd(DIR):
            logging.info(f"Actual directory changed to: {DIR}")
            logging.info(f"Downloading {REMOTE_FILE}")
            sftp.get(REMOTE_FILE, "out/output.sql")
            logging.info(f"Download complete")
    return True
  except Exception:
    logging.error("Cannot download the remote file")
    return False

def reload_database():
  '''
  Create the database if not exists
  '''
  logging.info("Reloading database")

  try:
    db = pymysql.connect(LOCAL_DB_HOST, LOCAL_DB_USER, LOCAL_DB_PASSWORD)
    cursor = db.cursor()
    cursor.execute("USE information_schema")
    cursor.execute('SELECT COUNT(*) FROM schemata WHERE SCHEMA_NAME=%s', (LOCAL_DB_NAME))
    result = cursor.fetchone()

    if(result[0] >= 1):
      logging.info("The database exists. Executing DROP DATABASE")
      cursor.execute("DROP DATABASE "+ LOCAL_DB_NAME +";")
    else:
      logging.info("The database does not exists. Trying to create")

    cursor.execute("CREATE DATABASE "+ LOCAL_DB_NAME)
    logging.info(f"Database {LOCAL_DB_NAME} created")

    db.close()
    return True
  except Exception:
    logging.error("Cannot reload the database. Please, check the connection details in env.py")
    return False

  
def dump():
  # Remove .lnk if your Windows terminal recognize it in a different way.
  try:
    if(SYSTEM == 'linux'):
      os.system('mysql --host="'+LOCAL_DB_HOST+'" --user="'+LOCAL_DB_USER+'" --password="'+LOCAL_DB_PASSWORD+'" '+ LOCAL_DB_NAME +' < out/output.sql') 
      #logging.info('mysql --host="'+LOCAL_DB_HOST+'" --user="'+LOCAL_DB_USER+'" --password="'+LOCAL_DB_PASSWORD+'" '+ LOCAL_DB_NAME +' < out/output.sql')
    else:  #Should be windows
      os.system('cmd /k "mysql.lnk --host="'+LOCAL_DB_HOST+'" --user="'+LOCAL_DB_USER+'" --password="'+LOCAL_DB_PASSWORD+'" '+ LOCAL_DB_NAME +' < out/output.sql"') 

    logging.info("Database dumped")
    return True
  except Exception:
    logging.error("Cannot dump the database into MySQL. Check if your mysqldump work properly from the command line inside this folder")
    return False


def main():
  logging.basicConfig(filename='log/'+ datetime.today().strftime('%Y%m%d_%H%M%S') +'.log', filemode='w', format='%(asctime)s %(levelname)s - %(message)s', datefmt='%Y%m%d %H:%M:%S', level=logging.INFO)
  logging.info("Running...")
  
  if not reload_database() or not dump(): 
    print("Error during the process. Check the log files.")
    return
  
  logging.info("The process finished with no errors")

if __name__ == "__main__":
  main()
