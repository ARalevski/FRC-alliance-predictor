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

# %%
# Collecting EVENT data

starting_year = 2019

# Collecting frc event keys
frc_event_keys = []

# Gets event response from api
event_response = requests.get(api_url + '/events/' + str(starting_year) + '/simple', headers=headers)
raw_event_data = event_response.json()

index = 0
# Ensures the collection stops when there is no more events left to gather
while len(raw_event_data) > 0 and 'Errors' not in raw_event_data:
    print("On year " + str(starting_year + index) + "... Collecting ...")

    for event in raw_event_data:
        frc_event_keys.append(event["key"])

    index += 1
    event_response = requests.get(api_url + '/events/' + str(starting_year + index) + "/simple", headers=headers)
    raw_event_data = event_response.json()

# Collect OPRS data from events

# Rows of OPRS dataframe
rows_list = []

for event_key in frc_event_keys:
    print("Gathering from " + event_key)

    # Gets OPRS response from api
    oprs_response = requests.get(api_url + '/event/' + event_key + "/oprs", headers=headers)
    raw_oprs_data = oprs_response.json()

    # Extracting MATCH and formatting data
    for oprs in raw_oprs_data:
        row = {}

        row['ccwms'] = oprs['ccwms']
        row['dprs'] = oprs['dprs']
        row['oprs'] = oprs['oprs']

        rows_list.append(row)

# Turns row list into dataframe
oprs_df = pd.DataFrame(rows_list)

# Saves matches dataframe to csv file
oprs_df.to_csv('raw_frc_oprs.csv')
