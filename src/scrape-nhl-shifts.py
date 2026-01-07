import pandas as pd
import requests

def get_team_id_for_player_id(roster_data, player_id):
    """
    Returns the teamId for a given player_id from the roster data.
    
    Args:
        roster_data (dict): The full roster data containing 'rosterSpots' list.
        player_id (int): The player ID to look up.
    
    Returns:
        int or None: The teamId if the player is found, otherwise None.
    """
    print(f"Fetching teamId for player_id: {player_id}")
    
    for spot in roster_data:
        if spot.get("playerId") == player_id:
            team_id = spot.get("teamId")
            print(f"Found player {player_id} on team {team_id}")
            return team_id
    
    # Player not found
    print(f"Player with player_id {player_id} not found in roster")
    return None


def get_shift_end_reason_for_goal(scoring_team_id, player_team_id):
    if scoring_team_id == player_team_id:
        return 'goal-for'
    else:
        return 'goal-against'

# request nhl shift api
nhl_shift_api = 'https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId=2021020001'
nhl_shift_response = requests.get(nhl_shift_api)
if nhl_shift_response.status_code != 200:
        print(f"Error: {nhl_shift_response.status_code} - {nhl_shift_response.text}")        
nhl_shift_json = nhl_shift_response.json()
df_nhl_shifts = pd.DataFrame(nhl_shift_json['data'],  columns=['id', 'gameId', 'playerId', 'detailCode', 'duration', 'startTime', 'endTime', 'period', 'shiftNumber', 'teamAbbrev'])
# print(df_nhl_shifts)

nhl_event_api = 'https://api-web.nhle.com/v1/gamecenter/2021020001/play-by-play'
nhl_event_response = requests.get(nhl_event_api)
if nhl_event_response.status_code != 200:
        print(f"Error: {nhl_event_response.status_code} - {nhl_event_response.text}")        
nhl_event_json = nhl_event_response.json()
df_nhl_events = pd.DataFrame(nhl_event_json['plays'], columns=['timeInPeriod', 'typeDescKey', 'periodDescriptor', 'details' ])

rosters = nhl_event_json['rosterSpots']

get_team_id_for_player_id
## ScoringTeamId = eventOwnerId

df_nhl_events['period'] = df_nhl_events['periodDescriptor'].apply(lambda x: x['number'])

# event stoppages dataframes
df_stoppages = df_nhl_events[
        df_nhl_events['typeDescKey'].isin(['goal', 'stoppage'])
].copy()
# Create new column safely (handles cases where 'details' might be NaN or missing 'reason')
df_stoppages['stoppage_reason_one'] = df_stoppages['details'].apply(
    lambda x: x.get('reason') if isinstance(x, dict) and 'reason' in x else isinstance(x, dict) and 'reason'
    
)
df_stoppages['stoppage_reason_two'] = df_stoppages['details'].apply(
    lambda x: x.get('secondaryReason') if isinstance(x, dict) and 'secondaryReason' in x else None
)

# === Fill null values with "other" ===
df_stoppages['typeDescKey'] = df_stoppages['typeDescKey'].fillna('other')
df_stoppages['stoppage_reason_one'] = df_stoppages['stoppage_reason_one'].fillna('other')
df_stoppages = df_stoppages.drop(columns=['periodDescriptor', 'details'])


df_shift_stoppages = df_nhl_shifts.merge(
    df_stoppages,
    left_on=['endTime', 'period'],
    right_on=['timeInPeriod', 'period'],
    how='left'
)

df_shift_stoppages.to_csv('shift-stoppages.csv', index=False)