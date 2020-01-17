import requests
import json
import sys

class Sleeper:
  def __init__(self):
    self.fetch_count = 0
  
  # how do league ids change per year? New league id for each year
  def getLeagueMatchupsStats(self, week, league_id):
    sleeper_url = "https://api.sleeper.app/v1/league/" + league_id + "/matchups/" + str(week)
    response = requests.get(sleeper_url)
    filename = "leagues/" + league_id + "/week" + str(week) + "_matchups.json"
    self.fetch_count += 1

  def getLeagueSettings(self, league_id):
    sleeper_url = "https://api.sleeper.app/v1/league/" + league_id # investigate if there is a /settings endpoint
    response = requests.get(sleeper_url)
    filename = "leagues/" + league_id + "/settings.json"
    self.fetch_count += 1

  def getLeagueUsers(self, league_id):
    sleeper_url = "https://api.sleeper.app/v1/league/" + league_id + "/users"
    response = requests.get(sleeper_url)
    self.fetch_count += 1
    return response.json()

  def getLeagueRosters(self, league_id):
    sleeper_url = "https://api.sleeper.app/v1/league/" + league_id + "/rosters"
    response = requests.get(sleeper_url)
    filename = "leagues/" + league_id + "/rosters.json"
    self.fetch_count += 1
    return response.json()

  def getDraft(self, league_id, draft_id):
    sleeper_url = "https://api.sleeper.app/v1/draft/" + draft_id + "/picks"
    response = requests.get(sleeper_url)
    filename = "leagues/" + league_id + "/draft.json"
    self.fetch_count += 1

  def getUser(self, username):
    sleeper_url = "https://api.sleeper.app/v1/user/" + username
    response = requests.get(sleeper_url)
    self.fetch_count += 1
    return response.json();

  def getLeagues(self, user_id, season):
    sleeper_url = "https://api.sleeper.app/v1/user/" + user_id + "/leagues/nfl/" + str(season)
    response = requests.get(sleeper_url)
    self.fetch_count += 1
    return response.json()

def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)
  outfile.close()

# fetchAllPlayers is a one time fetch for each week post stat corrections, contains stats for each player
# fetchAllPlayers(3)
# fetchMatchupsStats(3)

# Init League -> gather league settings if not exist
# Fetch Matchup for week and pull stats for that week and year
# Generate Output