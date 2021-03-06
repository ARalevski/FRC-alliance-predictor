import json
import requests
import pandas as pd


# Sets up variables for data collection from api
api_key = "API-KEY"
api_url = "https://www.thebluealliance.com/api/v3"

headers = {
    'Content-Type': 'application/json',
    'X-TBA-Auth-Key': api_key
}

# Collecting TEAM data

# Rows list is used to store all the data before its turned into a dataframe
rows_list = []

# Gets team response from api
response = requests.get(api_url + '/teams/0', headers=headers)
raw_data = response.json()

index = 0
# Ensures the collection stops when there is no more teams left to gather
while len(raw_data) > 0:
    print("On page " + str(index) + "...")

    for team in raw_data:
        row = {}

        for key, value in team.items():
            row[key] = value

        rows_list.append(row)

    # Iterates through the team list
    index += 1
    response = requests.get(api_url + '/teams/' + str(index), headers=headers)
    raw_data = response.json()

# Turns row list into a dataframe
team_df = pd.DataFrame(rows_list)

# Saves teams dataframe to csv file
team_df.to_csv('raw_frc_teams.csv')

# %%
# Collecting MATCH data

starting_year = 2019

# Collecting frc event keys
frc_event_keys = []

# Gets event response from api
event_response = requests.get(api_url + '/events/' + str(starting_year) + '/simple', headers=headers)
raw_event_data = event_response.json()

index = 0
# Ensures the collection stops when there is no more teams left to gather
while len(raw_event_data) > 0 and 'Errors' not in raw_event_data:
    print("On year " + str(starting_year + index) + "... Collecting ...")

    for event in raw_event_data:
        frc_event_keys.append(event["key"])

    index += 1
    event_response = requests.get(api_url + '/events/' + str(starting_year + index) + "/simple", headers=headers)
    raw_event_data = event_response.json()

# Collect MATCH data from events

# Rows of MATCH dataframe
rows_list = []

for event_key in frc_event_keys:
    print("Gathering from " + event_key)

    # Gets MATCH response from api
    match_response = requests.get(api_url + '/event/' + event_key + "/matches/simple", headers=headers) #changed to /matches rather than /matches/simple
    raw_match_data = match_response.json()

    # Extracting MATCH and formatting data
    for match in raw_match_data:
        row = {}

        for key, value in match.items():
            if key == 'alliances':
                # Gather data for red alliance
                red_alliance = match[key]['red']

                row['red_score'] = red_alliance['score']
                for i in range(len(red_alliance['team_keys'])):
                    row['red_' + str(i)] = red_alliance['team_keys'][i]

                # Gather data for blue alliance
                blue_alliance = match[key]['blue']

                row['blue_score'] = blue_alliance['score']
                for i in range(len(blue_alliance['team_keys'])):
                    row['blue_' + str(i)] = blue_alliance['team_keys'][i]
            else:
                row[key] = match[key]

        rows_list.append(row)

# Turns row list into dataframe
match_df = pd.DataFrame(rows_list)

# Saves matches dataframe to csv file
match_df.to_csv('raw_frc_matches.csv')

#Collecting ROBOTS data

#Collect all frc team keys first
frc_team_keys = []

# Gets TEAM response from api
response = requests.get(api_url + '/teams/0', headers=headers)
raw_data = response.json()

index = 0
# Ensures the collection stops when there is no more teams left to gather
while len(raw_data) > 0:
    print("On page " + str(index) + "...")

    for team in raw_data:
        frc_team_keys.append(team['key'])

    # Iterates through the team list
    index += 1
    response = requests.get(api_url + '/teams/' + str(index), headers=headers)
    raw_data = response.json()

# Rows list is used to store all the data before its turned into a dataframe
rows_list = []

for team_key in frc_team_keys:
    print('Getting robots for team ' + team_key)

    # Gets team response from api
    response = requests.get(api_url + '/team/' + team_key + "/robots", headers=headers)
    raw_robot_data = response.json()

    for robot in raw_robot_data:
        row = {}

        row['key'] = robot['key']
        row['robot_name'] = robot['robot_name']
        row['team_key'] = team_key
        row['year'] = robot['year']

        rows_list.append(row)

robot_df = pd.DataFrame(rows_list)

robot_df.to_csv('raw_frc_robots.csv')






