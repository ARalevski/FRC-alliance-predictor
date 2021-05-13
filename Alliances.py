import json
import requests
import pandas as pd

api_key = "API-KEY"
api_url = "https://www.thebluealliance.com/api/v3"

headers = {
    'Content-Type': 'application/json',
    'X-TBA-Auth-Key': api_key
}

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

#Get alliance data
rows_list = []
 
for event_key in frc_event_keys:
    print("Gathering from " + event_key)

    # Gets MATCH response from api
    alliance_response = requests.get(api_url + '/event/' + event_key + "/alliances", headers=headers)
    raw_alliance_data = alliance_response.json()

    # Extracting MATCH and formatting data
    for alliance in raw_alliance_data:
        row = {}

        for key, value in alliance.items():
            if key == 'name':
                # Gather data for Alliance 1
                alliance_1 = alliance[key]['Alliance 1']

                for i in range(len(alliance_1['picks'])):
                    row['alliance_1_' + str(i)] = alliance_1['picks'][i]

                row['win_status'] = alliance_1['status']

            else:
                row[key] = alliance[key]

        rows_list.append(row)

# Turns row list into dataframe
alliance_df = pd.DataFrame(rows_list)

# Saves matches dataframe to csv file
alliance_df.to_csv('raw_frc_alliances.csv')