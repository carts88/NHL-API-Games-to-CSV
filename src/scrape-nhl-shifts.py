import pandas as pd
import requests

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