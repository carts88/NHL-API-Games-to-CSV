import pandas as pd
import requests
import csv

coach_bio_url = 'https://records.nhl.com/site/api/coach'
coach_tenure_api_url = 'https://records.nhl.com/site/api/coach-franchise-records?cayenneExp=gameTypeId=2&include=coach.id'

def get_json_for_api(api_endpoint: str):
    response = requests.get(api_endpoint)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    else: 
        return response.json()

coach_bio_json = get_json_for_api(coach_bio_url)
if not coach_bio_json:
    raise ValueError("Failed to retrieve coach bio data")
coach_bio_data = coach_bio_json.get('data', [])
print(f"Retrieved {len(coach_bio_data)} coaches")


coach_tenure_json = get_json_for_api(coach_tenure_api_url)
if not coach_tenure_json:
    raise ValueError("Failed to retrieve coach tenure data")

coach_tenure_data = coach_tenure_json.get('data', [])
print(f"Retrieved {len(coach_tenure_data)} coach tenures")

# Create the DataFrame with only the columns you need
df_coach_tenures = pd.DataFrame({
    'nhl_id': [item['coach']['id'] for item in coach_tenure_data],
    'start_date': [item['firstCoachedDate'] for item in coach_tenure_data],
    'end_date': [item['lastCoachedDate'] for item in coach_tenure_data],
    'team': [item['teamAbbrev'] for item in coach_tenure_data],
    'role': 'head_coach'
})


# First, create the bio DataFrame and a mapping from nhl_id to staff_id
coach_bio_list = []
nhl_id_to_staff_id = {}  # This will map NHL coach ID → your custom staff_id

for increment, coach in enumerate(coach_bio_data, start=1):
    staff_id = f"CCSTA1_{increment}"
    
    coach_id = coach.get('id')  # This is the NHL coach ID (nhl_id)
    first_name = coach.get('firstName')
    last_name = coach.get('lastName')
    
    # Store the mapping
    nhl_id_to_staff_id[coach_id] = staff_id
    
    full_name = f"{coach.get('firstName')} {coach.get('lastName')}"
    
    if coach_id and first_name and last_name not in coach:
        coach_row = [
            coach_id,                   # original NHL coach ID
            coach.get('playerId'),      # linked player ID if former player
            coach.get('firstName'),
            coach.get('lastName'),
            coach.get('birthDate'),
            coach.get('dateOfDeath'),
            coach.get('birthCity'),
            coach.get('birthCountrycode'),
            coach.get('birthStateProvinceCode'),
            coach.get('nationalityCode'),
        ]
        coach_bio_list.append(coach_row)

# Create the bios DataFrame
columns = [
    "nhl_id", "player_id", "first_name", "last_name",
    "birthdate", "date_of_death", "birth_city",
    "birth_country_code", "birth_state_province_code", "nationality_code",
]
df_coach_bios = pd.DataFrame(coach_bio_list, columns=columns)
df_coach_bios["player_id"] = df_coach_bios["player_id"].astype("Int64")

# Add staff_id to the bios
df_coach_bios["staff_id"] = df_coach_bios["nhl_id"].map(nhl_id_to_staff_id)

# Now create the tenures DataFrame with the correct staff_id
df_coach_tenures = pd.DataFrame({
    'nhl_id': [item['coach']['id'] for item in coach_tenure_data],
    'start_date': [item['firstCoachedDate'] for item in coach_tenure_data],
    'end_date': [item['lastCoachedDate'] for item in coach_tenure_data],
    'team': [item['teamAbbrev'] for item in coach_tenure_data],
    'role': ['head_coach' for item in coach_tenure_data]
})

# Add the staff_id by mapping nhl_id
df_coach_tenures["staff_id"] = df_coach_tenures["nhl_id"].map(nhl_id_to_staff_id)

# Optional: reorder columns
df_coach_tenures = df_coach_tenures[['staff_id', 'nhl_id', 'start_date', 'end_date', 'team', 'role']]

# Save both
df_coach_bios.to_csv("head_coach_bios.csv", index=False)
df_coach_tenures.to_csv("head_coach_tenures.csv", index=False, quoting=csv.QUOTE_MINIMAL)



print("Saved head_coach_bios.csv and head_coach_tenures.csv with matching staff_id")