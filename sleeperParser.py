# not currently supporting IDP FLEX, DL, LB, DB
all_positions = ['QB', 'RB', 'WR', 'TE', 'FLEX', 'SUPER_FLEX', 'DEF', 'K', 'BN', 'REC_FLEX', 'DL', 'WRRB_FLEX', 'DB', 'LB', 'IDP_FLEX']
 
def get_user_id(sleeperFetches, username):
  user_data = sleeperFetches.getUser(username)
  # need to verfiy or be alerted if this id doesn't exist
  if not user_data:
    return ''
  return user_data['user_id']

def get_leagues(sleeperFetches, user_id, year):
  user_leagues = sleeperFetches.getLeagues(user_id, year)
  leagues = []
  for league in user_leagues:
    if league['sport'] == "nfl":
      l_settings = [
        league['league_id'],
        league['name'],
        league['total_rosters'],
        'sleeper',
        league['season'], # league id is per year basis for sleeper
        league['season_type']
        # "draft_id": league['draft_id'],
        # "avatar": league['avatar']
      ]
      roster_positions = parseRosterPositions(league['roster_positions'])
      leagues.append(tuple(l_settings + roster_positions))
  return leagues

def parseRosterPositions(roster_spots): 
  positions_count = []
  for rp in all_positions:
    positions_count.append(roster_spots.count(rp))
  for rp in roster_spots:
    if rp not in all_positions:
      print(rp, 'not in table')
  return positions_count
  
def get_league_rosters(sleeperFetches, league_id):
  rosters = sleeperFetches.getLeagueRosters(league_id)
  settings = ['wins', 'ties', 'fpts', 'losses', 'fpts_against']
  fields = ['owner_id', 'league_id', 'roster_id']
  data = []
  for roster in rosters:
    setting_fields = list(map(lambda x: roster['settings'][x], settings))
    roster_fields = list(map(lambda x: roster[x], fields))
    data.append(tuple(roster_fields + setting_fields))
  return data

def get_league_users(sleeperFetches, league_id):
  users = sleeperFetches.getLeagueUsers(league_id)
  data = []
  fields = ['user_id', 'display_name']
  for user in users:
    user_fields = list(map(lambda x: user[x], fields))
    data.append(tuple(user_fields))
  return data
