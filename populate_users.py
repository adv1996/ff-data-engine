import sqlite3
from sqlite3 import Error
import json
import sleeperParser
import sleeperFetches as sleeper # need to change value of sleeperFetches
from time import perf_counter 

# these should be aws lambdas in the future
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
  sql = ''' INSERT OR IGNORE INTO Users(user_id,username)
            VALUES(?,?) '''
  cur = conn.cursor()
  cur.execute(sql, user)
  return cur.lastrowid

def add_users(conn, users):
  sql = ''' INSERT OR IGNORE INTO Users(user_id,username)
            VALUES(?,?) '''
  cur = conn.cursor()
  cur.executemany(sql, users)

def add_leagues(conn, leagues):
  sql = ''' INSERT OR IGNORE INTO Leagues(league_id,league_name,total_rosters,platform,season,season_type,QB,RB,WR,TE,FLEX,SUPER_FLEX,DEF,K,BN,REC_FLEX,DL,WRRB_FLEX,DB,LB,IDP_FLEX)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
  cur = conn.cursor()
  cur.executemany(sql, leagues)

def add_userLeague(conn, league_users):
  sql = ''' INSERT OR IGNORE INTO UserLeague(user_id,league_id, roster_id, wins, ties, fpts, losses, fpts_against)
            VALUES(?,?,?,?,?,?,?,?) '''
  cur = conn.cursor()
  cur.executemany(sql, league_users)

def get_user_league_pairs(leagues, user_id):
  league_user_pairs = []
  for league in leagues:
    league_user_pairs.append((
      user_id,
      league[0]
    ))
  return league_user_pairs

def main():
  database = r"ffDB.db" # use an env variable for this

  # create a database connection
  conn = create_connection(database)
  t1_start = perf_counter()  
  sleeperFetches = sleeper.Sleeper()
  usernames = []
  # note: if this fails then SQL doesn't push
  with conn:
    # TODO right now we are updating the database for each user, should combine all the calls so that only 1 push for all
    for username in usernames:
      league_rosters = []
      league_users_total = []
      # 1. Get Username
      # 2. Get User_ID
      user_id = sleeperParser.get_user_id(sleeperFetches, username)
      user = (user_id, username);
      print(user)
      if user_id:
        # 3. Check if User_Id in Table
        # 4. Add User to Users Table
        add_user(conn, user)
        # 5. Get League ID and League Information
        leagues = sleeperParser.get_leagues(sleeperFetches, user_id, 2019)
        # 6. Add League Information to Leagues Table
        add_leagues(conn, leagues)
        # 7. Get League Members and Load them into UserPairs
        # TODO optimize this, can get rid of user_league_pairs with lambda in place, just need league ids
        user_league_pairs = get_user_league_pairs(leagues, user_id)
        for user_league in user_league_pairs:
          league_id = user_league[1]
          # TODO log errors to track incorrect league imports
          league_roster = sleeperParser.get_league_rosters(sleeperFetches, league_id)
          league_rosters = league_rosters + league_roster

          # 8. Get /users and load leaguemates into Users Table
          league_users = sleeperParser.get_league_users(sleeperFetches, league_id)
          league_users_total = league_users_total + league_users
        add_userLeague(conn, league_rosters)
        add_users(conn, league_users_total)
  conn.close()
  t1_stop = perf_counter() 
  print(sleeperFetches.fetch_count, 'calls in', t1_stop - t1_start, 'seconds')
def parse_espn_users():
  # file needs to be relative
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

def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)
  outfile.close()
  print('Successfully save file', len(data), 'records!')

if __name__ == '__main__':
  main()