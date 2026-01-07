# External Library Imports
import pandas as pd
from datetime import date, datetime
from zoneinfo import ZoneInfo  # Python 3.9+

# Python Imports
import requests
import sys
import os

# Internal Imports
sys.stdout.reconfigure(encoding="utf-8")

draft_years = [1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

# EST-aware timestamp for filenames
timestamp = datetime.now(ZoneInfo("America/New_York")).strftime("%Y%m%d_%H%M%S")
today = date.today().isoformat()  # 'YYYY-MM-DD'
# Ensure output directory exists
output_dir = f"data/{today}"
os.makedirs(output_dir, exist_ok=True)

# functions

def get_draft_url(year: int):
    return f"https://records.nhl.com/site/api/draft?cayenneExp=%20draftYear%20=%20{str(year)}"

def get_position_group(position):
    if position == 'G':
        return 'goalie'
    elif position == 'D':
        return 'defenseman'
    else:
        return 'forward'

def format_number_suffix(number: int):
    """
    Returns the English ordinal suffix for a given integer.
    
    Examples:
        1  -> "st"
        2  -> "nd"
        3  -> "rd"
        11 -> "th"
        12 -> "th"
        13 -> "th"
        21 -> "st"
        22 -> "nd"
        23 -> "rd"
        24 -> "th"
    """
    # Handle the absolute value to deal with negative numbers correctly
    abs_number = abs(number)
    
    # Get the last two digits to check for teen exceptions (11, 12, 13)
    last_two = abs_number % 100
    
    if 11 <= last_two <= 13:
        return f"{number}th"
    
    # Get the last digit
    last_digit = abs_number % 10
    
    if last_digit == 1:
        return f"{number}st"
    elif last_digit == 2:
        return f"{number}nd"
    elif last_digit == 3:
        return f"{number}rd"
    else:  # 0, 4-9
        return f"{number}th"    

def create_drafted_player_note(
    draft_date,
    full_name,
    position, 
    draft_year,
    draft_round,
    draft_overall_pick,
    current_owner,  # drafted by
    original_owner,  # the original owner of the pick used to draft player
    amateur_team,
    amateur_league,
):
    original_owner_part = ""
    if current_owner != original_owner:
        original_owner_part = f" (originally owned by {original_owner})"
    
    note = (
        f"On {draft_date}, with the {format_number_suffix(draft_overall_pick)} overall pick "
        f"in the {format_number_suffix(draft_round)} round of the {draft_year} draft{original_owner_part}, "
        f"{current_owner} selected {full_name}, a {amateur_league} {get_position_group(position)} "
        f"playing for {'the ' if amateur_team and amateur_team.rstrip().endswith('s') else ''}{amateur_team}."
        )
    return note


historical_compensation_pick_ids = [
    ''
]

# initialized data lists
draft_picks_data = []
draft_pick_transactions = []
no_draft_pick_player_id = []

# main loop
for year in draft_years:
    draft_api_url = get_draft_url(year)
    draft_api_response = requests.get(draft_api_url)
    if draft_api_response.status_code != 200:
        print(f"Error fetching draft data for year {year}: {draft_api_response.status_code}")
        continue
    
    draft_year_json = draft_api_response.json()
    draft_year = year
    draft_picks = draft_year_json.get('data', [])
    
    for pick in draft_picks:
        teamPickHistory = pick.get('teamPickHistory', '')  # Safely get the value, default to empty string if missing
        
        player_id = pick.get('playerId')

        drafted_date = pick.get('draftDate')
        full_name = pick.get('playerName', '')
        position = pick.get('position')
        draft_round = pick.get('roundNumber', '')
        draft_overall_pick = pick.get('overallPickNumber')
        original_owner = teamPickHistory[:3]  # Slice the first 3 characters
        current_owner = pick.get('triCode', '')
        pick_id = f"{draft_year}-{original_owner}-{draft_round}"
        transaction_id = f"{pick_id}-{player_id}"
        amateur_league = pick.get('amateurLeague')
        amateur_team = pick.get('amateurClubName')
        draft_note = create_drafted_player_note(
            drafted_date,
            full_name,
            position, 
            draft_year,
            draft_round,
            draft_overall_pick,
            current_owner, # drafted by
            original_owner, # the original owner of the pick used to draft player
            amateur_team,
            amateur_league
        )


        if player_id != 4044:
            draft_pick_transaction = [
                transaction_id,
                player_id,
                current_owner,
                "DRAFTED",
                drafted_date,
                draft_note
            ]
            draft_pick_transactions.append(draft_pick_transaction)
        
        if not player_id:
            player_id = 4044
      
        draftPick = [
            pick_id,
            draft_year,
            draft_round,
            draft_overall_pick,
            original_owner,
            current_owner,
            player_id,
            pick.get('pickInRound'),
        ]
        draft_picks_data.append(draftPick)
        


# Draft Transaction Based Data Cleaning & CSV Exporting
df_transactions = pd.DataFrame(
    draft_pick_transactions,
    columns=["transaction_id", "player_id", "tricode", "type", "date", "notes"]
)

# Drop rows where player_id is missing (or was set to placeholder), if desired
df_transactions = df_transactions.dropna(subset=["player_id"])

# CRITICAL FIX: Convert player_id to Int64 (pandas nullable integer type) to avoid .0
df_transactions["player_id"] = df_transactions["player_id"].astype("Int64")

# Now save — player_id will appear as clean integers (e.g., 8471234, not 8471234.0)
df_transactions.to_csv(f"{output_dir}/draft_picks_transactions_{timestamp}.csv", index=False)

# Draft Pick Based Data Cleaning & CSV Exporting

df = pd.DataFrame(draft_picks_data, columns=[
    "pick_id", "draft_year", "draft_round", "draft_overall", 
    "original_owner", "current_owner", "drafted_player_id", "pick_in_round"
])
# Create per-pick index (0, 1, 2, ...)
df['pick_id_index'] = df.groupby('pick_id').cumcount()

# Only append index when there are duplicates
df['pick_id'] = df['pick_id'] + df['pick_id_index'].add(1).astype(str).radd('-').where(
    df['pick_id_index'] > 0, ''
)

# Drop helper column
df.drop(columns=['pick_id_index'], inplace=True)

df.to_csv(f"{output_dir}/draft_picks_{timestamp}.csv", index=False)
