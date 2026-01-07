import pandas as pd
import requests
import csv


gm_tenure_api_url = 'https://records.nhl.com/site/api/general-manager-franchise-records?&include=generalManager.id&include=team.triCode'
gm_bio_url = 'https://records.nhl.com/site/api/general-manager/'


def get_json_for_api(api_endpoint: str):
    response = requests.get(api_endpoint)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    else: 
        return response.json()

gm_bio_json = get_json_for_api(gm_bio_url)
if not gm_bio_json:
    raise ValueError("Failed to retrieve gm bio data")
gm_bio_data = gm_bio_json.get('data', [])
print(f"Retrieved {len(gm_bio_data)} gmes")


gm_tenure_json = get_json_for_api(gm_tenure_api_url)
if not gm_tenure_json:
    raise ValueError("Failed to retrieve gm tenure data")

gm_tenure_data = gm_tenure_json.get('data', [])
print(f"Retrieved {len(gm_tenure_data)} gm tenures")

# Create the DataFrame with only the columns you need
df_gm_tenures = pd.DataFrame({
    'nhl_id': [item['generalManager']['id'] for item in gm_tenure_data],
    'start_date': [item['startDate'] for item in gm_tenure_data],
    'end_date': [item['endDate'] for item in gm_tenure_data],
    'team': [item['team']['triCode'] for item in gm_tenure_data],
    'role': 'general_manager'
})


# First, create the bio DataFrame and a mapping from nhl_id to staff_id
gm_bio_list = []
nhl_id_to_staff_id = {}  # This will map NHL gm ID → your custom staff_id

for increment, gm in enumerate(gm_bio_data, start=1):
    staff_id = f"CCSTA2_{increment}"
    
    gm_id = gm.get('id')  # This is the NHL gm ID (nhl_id)
    first_name = gm.get('firstName')
    last_name = gm.get('lastName')
    
    # Store the mapping
    nhl_id_to_staff_id[gm_id] = staff_id
    
    full_name = f"{gm.get('firstName')} {gm.get('lastName')}"
    
    if gm_id and first_name and last_name not in gm:
        gm_row = [
            gm_id,                   # original NHL gm ID
            gm.get('playerId'),      # linked player ID if former player
            gm.get('firstName'),
            gm.get('lastName'),
            gm.get('birthDate'),
            gm.get('dateOfDeath'),
            gm.get('birthCity'),
            gm.get('birthCountrycode'),
            gm.get('birthStateProvinceCode'),
            gm.get('nationalityCode'),
        ]
        gm_bio_list.append(gm_row)

# Create the bios DataFrame
columns = [
    "nhl_id", "player_id", "first_name", "last_name",
    "birthdate", "date_of_death", "birth_city",
    "birth_country_code", "birth_state_province_code", "nationality_code",
]
df_gm_bios = pd.DataFrame(gm_bio_list, columns=columns)
df_gm_bios["player_id"] = df_gm_bios["player_id"].astype("Int64")

# Add staff_id to the bios
df_gm_bios["staff_id"] = df_gm_bios["nhl_id"].map(nhl_id_to_staff_id)

# Add the staff_id by mapping nhl_id
df_gm_tenures["staff_id"] = df_gm_tenures["nhl_id"].map(nhl_id_to_staff_id)

# Optional: reorder columns
df_gm_tenures = df_gm_tenures[['staff_id', 'nhl_id', 'start_date', 'end_date', 'team', 'role']]

# Save both
df_gm_bios.to_csv("gm_bios.csv", index=False)
df_gm_tenures.to_csv("gm_tenures.csv", index=False, quoting=csv.QUOTE_MINIMAL)