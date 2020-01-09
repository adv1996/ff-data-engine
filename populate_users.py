import sqlite3
from sqlite3 import Error
import json
import sleeperFetches

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
  sql = ''' INSERT INTO users(user_id,username)
            VALUES(?,?) '''
  cur = conn.cursor()
  cur.execute(sql, user)
  return cur.lastrowid

def add_users(conn, users):
  """
  Create a new project into the projects table
  :param conn:
  :param project:
  :return: project id
  """
  sql = ''' INSERT INTO users(user_id,username)
            VALUES(?,?) '''
  cur = conn.cursor()
  cur.executemany(sql, users)

def main():
  database = r"ffDB.db" # use an env variable for this

  # create a database connection
  conn = create_connection(database)
  with conn:
    # add a new user
    # we will only add a new user if the user does not exist in the db prior
    # user = ('94862074874052608','adv1996');
    # users = parse_espn_users()
    # add_users(conn, users)
    # TODO figure out way to use same database connection to either add users,
    # or retrieve values for backup
    backup_users_table(conn)
  conn.close()

def parse_espn_users():
  espn_user_file = './example_outputs/espn_team.json'
  data = []
  with open(espn_user_file) as json_file:
    data = json.load(json_file)
  json_file.close()
  
  player_data = []
  if 'members' in data: # how to better determine if data exists
    for player in data['members']:
      player_data.append((
        player['id'],
        player['displayName'],
      ))
      # how can we make this more extensible to be as flexible for other platforms
  return player_data

def backup_users_table(conn):
  fields = ['user_id', 'username']
  # should select exact fields instead of *
  sql = ''' SELECT * FROM users '''
  cur = conn.cursor()
  cur.execute(sql)
  
  rows = cur.fetchall()
  data = []
  for row in rows:
    data.append({
      'user_id': row[0],
      'username': row[1]
    })
  saveJson('backup_users.json', data)

#TODO load backup data function, when should we backup data?

def get_leagues_sleeper(username):
  # first need to get user_id from username
  
def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)
  outfile.close()
  print('Successfully save file', len(data), 'records!')

if __name__ == '__main__':
  main()