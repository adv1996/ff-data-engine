import sqlite3
from sqlite3 import Error

def create_connection(db_file):
  """ create a database connection to the SQLite database
      specified by db_file
  :param db_file: database file
  :return: Connection object or None
  """
  conn = None
  try:
    conn = sqlite3.connect(db_file)
  except Error as e:
    print(e)

  return conn
  
def add_user(conn, user):
  """
  Create a new project into the projects table
  :param conn:
  :param project:
  :return: project id
  """
  sql = ''' INSERT INTO users(user_id,username,platform)
            VALUES(?,?,?) '''
  cur = conn.cursor()
  cur.execute(sql, user)
  return cur.lastrowid

def main():
  database = r"ffDB.db" # use an env variable for this

  # create a database connection
  conn = create_connection(database)
  with conn:
    # add a new user
    # we will only add a new user if the user does not exist in the db prior
    user = ('94862074874052608','adv1996', 'sleeper');
    user_id = add_user(conn, user)
    print(user_id)
 
 
if __name__ == '__main__':
  main()