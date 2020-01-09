import requests
import json
import sys

# deprecated
def fetchAllPlayers(year, week):
  sleeper_url = "https://api.sleeper.app/v1/stats/nfl/regular/" + year + "/" + str(week)
  print(sleeper_url)
  response = requests.get(sleeper_url)
  filename = "stats/" + str(year) + "w" + str(week) + ".json"
  saveJson(filename, response.json())

# how do league ids change per year?
def getLeagueMatchupsStats(week, league_id):
  sleeper_url = "https://api.sleeper.app/v1/league/" + league_id + "/matchups/" + str(week)
  response = requests.get(sleeper_url)
  filename = "leagues/" + league_id + "/week" + str(week) + "_matchups.json"
  saveJson(filename, response.json())

def getLeagueSettings(league_id):
  sleeper_url = "https://api.sleeper.app/v1/league/" + league_id
  response = requests.get(sleeper_url)
  filename = "leagues/" + league_id + "/settings.json"
  saveJson(filename, response.json())

def getLeagueUsers(league_id):
  sleeper_url = "https://api.sleeper.app/v1/league/" + league_id + "/users"
  response = requests.get(sleeper_url)
  filename = "leagues/" + league_id + "/users.json"
  saveJson(filename, response.json())

def getLeagueRosters(league_id):
  sleeper_url = "https://api.sleeper.app/v1/league/" + league_id + "/rosters"
  response = requests.get(sleeper_url)
  filename = "leagues/" + league_id + "/rosters.json"
  saveJson(filename, response.json())

def getDraft(league_id, draft_id):
  sleeper_url = "https://api.sleeper.app/v1/draft/" + draft_id + "/picks"
  response = requests.get(sleeper_url)
  filename = "leagues/" + league_id + "/draft.json"
  saveJson(filename, response.json())

def getUser(username):
  sleeper_url = "https://api.sleeper.app/v1/user/" + username
  response = requests.get(sleeper_url)
  filename = "sleeper/users/" + username + ".json"
  saveJson(filename, response.json())
  return response;

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