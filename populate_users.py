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
  sql = ''' INSERT INTO Users(user_id,username)
            VALUES(?,?) '''
  cur = conn.cursor()
  cur.execute(sql, user)
  return cur.lastrowid

def add_users(conn, users):
  sql = ''' INSERT INTO Users(user_id,username)
            VALUES(?,?) '''
  cur = conn.cursor()
  cur.executemany(sql, users)

def add_leagues(conn, leagues):
  sql = ''' INSERT INTO Leagues(league_id,league_name,total_rosters,platform,roster_positions,season,season_type)
            VALUES(?,?,?,?,?,?,?) '''
  cur = conn.cursor()
  cur.executemany(sql, leagues)

def add_leagues_to_user(leagues, user_id):
  league_user_pairs = []
  for league in leagues:
    league_user_pairs.append((
      user_id,
      league[0]
    ))
  return league_user_pairs

def add_userLeague(conn, league_users):
  sql = ''' INSERT INTO UserLeague(user_id,league_id)
            VALUES(?,?) '''
  cur = conn.cursor()
  cur.executemany(sql, league_users)

def main():
  database = r"ffDB.db" # use an env variable for this

  # create a database connection
  conn = create_connection(database)
  with conn:
    # add a new user
    # we will only add a new user if the user does not exist in the db prior
    # user = ('94862074874052608','adv1996');
    # users = parse_espn_users()
    # TODO figure out way to use same database connection to either add users,
    # or retrieve values for backup
    # backup_users_table(conn)
    # users = load_backup_users_table()
    # add_users(conn, users)
    user_id = "94862074874052608"
    leagues = get_leagues_sleeper("94862074874052608")
    # league_user_pairs = add_leagues_to_user(leagues, user_id)
    # add_userLeague(conn, league_user_pairs)
    
    add_leagues(conn, leagues)
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

def load_backup_users_table():
  backup_file = 'backup_users.json'
  data = []
  with open(backup_file) as json_file:
    data = json.load(json_file)
  json_file.close()
  users = []
  for row in data:
    # investigate if easier way to convert dict to tuple
    users.append((
      row['user_id'],
      row['username']
    ))
  return users;

def get_user_id_sleeper(username):
  user_data = sleeperFetches.getUser(username)
  # need to verfiy or be alerted if this id doesn't exist
  return user_data['user_id']

def get_leagues_sleeper(user_id):
  user_leagues = sleeperFetches.getLeagues(user_id, 2019)
  leagues = []
  for league in user_leagues:
    if league['sport'] == "nfl":
      leagues.append((
        league['league_id'],
        league['name'],
        league['total_rosters'], #need to use single value or migrate to Postgres
        'sleeper',
        ",".join(league['roster_positions']),
        league['season'], # league id is per year basis for sleeper
        league['season_type']
        # "draft_id": league['draft_id'],
        # "avatar": league['avatar']
      ))
  return leagues
  
def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)
  outfile.close()
  print('Successfully save file', len(data), 'records!')

if __name__ == '__main__':
  main()
  # get_leagues_sleeper("94862074874052608")