import requests
import csv
from datetime import datetime


""""
DATE: 12.26.2025
PLAN: Access base NHL player API https://api-web.nhle.com/v1/player/{player_id}, access seasonTotals.season if exists. If that season exists fetch game logs for that season, and imput them into player_game_logs.csv, once done fetching data for that player then fetch re-run same process for another player
"""

base_api = "https://api-web.nhle.com/v1"

team_codes = ['ANA', 'ARI']

skater_column_headers = [
    'game_id',
    'team_tricode',       # original (teamAbbrev maps to this)
    'date',               # original (gameDate maps to this)
    'season',             # original
    'home_road_flag',
    'goals',
    'assists',
    'team_nickname',
    'opponent_nickname',
    'points',
    'plus_minus',
    'power_play_goals',
    'power_play_points',
    'game_winning_goals',
    'ot_goals',
    'shots',
    'shifts',
    'shorthanded_goals',
    'shorthanded_points',
    'opponent_tricode',
    'pim',
    'toi'
]

goalie_column_headers = [
    'game_id',
    'team_tricode',       # from teamAbbrev
    'home_road_flag',
    'date',               # from gameDate
    'season',             # if you include it as before
    'goals',
    'assists',
    'common_name',
    'opponent_common_name',
    'games_started',
    'decision',
    'shots_against',
    'goals_against',
    'save_pctg',
    'shutouts',
    'opponent_abbrev',
    'pim',
    'toi'
]


def get_player_game_log_url(player_id: int, season_id: int, game_type_id: int):
    return f"https://api-web.nhle.com/v1/player/{player_id}/game-log/{season_id}/{game_type_id}"

def print_game_logs_to_csv(csvFileName: str, column_headers: list[str], game_logs: list[dict]):
    with open(csvFileName, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_headers)  # Header
        writer.writerows(game_logs)


# configuration values
skater_id_list = []
goalie_id_list = []
game_type_ids = [ 2, 3]

# initial empty data lists
skater_game_log_data = []
goalie_game_log_data = []
players_not_found = []
game_logs_not_found = []


for tricode in team_codes: 
    roster_api_url = f"{base_api}/roster/{tricode}/20242025"
    roster_api_response = requests.get(roster_api_url)

    if roster_api_response.status_code != 200:
        print(f"Error fetching roster for {tricode}: {roster_api_response.status_code}")
        continue
    roster_data = roster_api_response.json()
    
    for forward in roster_data.get('forwards', []):
        skater_id_list.append(forward['id'])
    for defenseman in roster_data.get('defensemen', []):
        skater_id_list.append(defenseman['id'])
    for goalie in roster_data.get('goalies', []):
        goalie_id_list.append(goalie['id'])
    


# big boy loop for goalies
for player_id in goalie_id_list:
    player_api_url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    player_api_response = requests.get(player_api_url)
    
    # If there is no response for that Player ID then it prints an error, and adds the playerId to a list, as well as skipping the rest of the iteration
    if player_api_response.status_code != 200:
        print(f"Error fetching data for player {player_id}: {player_api_response.status_code}")
        players_not_found.append(player_id) 
        continue
    
    player_data = player_api_response.json()
    
    # Optional: still check if it's a goalie (though your list is goalie_id_list)    
    # Only include seasons where the league is NHL
    season_ids = [
        season['season']  # or season['season'] if the key is 'season' – check actual JSON
        for season in player_data.get('seasonTotals', [])
        if season.get('leagueAbbrev') == 'NHL'  # common key based on NHL API patterns
    ]
    
    # If the key is 'gameTypeId' == 2 (regular season) or something else, adjust accordingly
    # But based on your description, it's likely 'leagueAbbrev' or similar for "NHL"
    
    # Then proceed with using season_ids, e.g., add to a master list or process further    
    for season_id in season_ids:
        for game_type_id in game_type_ids:
            game_log_for_season_api_url = get_player_game_log_url(player_id, season_id, game_type_id)
            game_log_for_season_response = requests.get(game_log_for_season_api_url)
            game_log_for_season_json = game_log_for_season_response.json()
            
            if 'gameLog' not in game_log_for_season_json:
                print(f"No gameLog data for player {player_id}, season {season_id}, game type {game_type_id}")
                game_logs_not_found.append((player_id, season_id, game_type_id))
                continue
            
            for game in game_log_for_season_json['gameLog']:
                    listing = [
                        game.get('gameId'),
                        game.get('teamAbbrev'),
                        game.get('homeRoadFlag'),
                        game.get('gameDate'),
                        season_id,
                        game.get('goals', 0),
                        game.get('assists', 0),
                        game.get('commonName.default', ''),
                        game.get('opponentCommonName.default', ''),
                        game.get('gamesStarted', 0),
                        game.get('decision', ''),
                        game.get('shotsAgainst', 0),
                        game.get('goalsAgainst', 0),
                        game.get('savePctg', 0.0),
                        game.get('shutouts', 0),
                        game.get('opponentAbbrev', ''),
                        game.get('pim', 0),
                        game.get('toi', '')
                    ]
                    goalie_game_log_data.append(listing)
                    print(f"Added game log for goalie {player_id}, season {season_id}, game type {game_type_id}")
print_game_logs_to_csv("goalie_game_logs.csv", goalie_column_headers, goalie_game_log_data)


for player_id in skater_id_list:
    player_api_url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    player_api_response = requests.get(player_api_url)
    
    # If there is no response for that Player ID then it prints an error, and adds the playerId to a list, as well as skipping the rest of the iteration
    if player_api_response.status_code != 200:
        print(f"Error fetching data for player {player_id}: {player_api_response.status_code}")
        players_not_found.append(player_id) 
        continue
    
    player_data = player_api_response.json()
    
    # Optional: still check if it's a goalie (though your list is goalie_id_list)    
    # Only include seasons where the league is NHL
    season_ids = [
        season['season']  # or season['season'] if the key is 'season' – check actual JSON
        for season in player_data.get('seasonTotals', [])
        if season.get('leagueAbbrev') == 'NHL'  # common key based on NHL API patterns
    ]
    
    # If the key is 'gameTypeId' == 2 (regular season) or something else, adjust accordingly
    # But based on your description, it's likely 'leagueAbbrev' or similar for "NHL"
    
    # Then proceed with using season_ids, e.g., add to a master list or process further    
    for season_id in season_ids:
        for game_type_id in game_type_ids:
            game_log_for_season_api_url = get_player_game_log_url(player_id, season_id, game_type_id)
            game_log_for_season_response = requests.get(game_log_for_season_api_url)
            game_log_for_season_json = game_log_for_season_response.json()
            
            if 'gameLog' not in game_log_for_season_json:
                print(f"No gameLog data for player {player_id}, season {season_id}, game type {game_type_id}")
                game_logs_not_found.append((player_id, season_id, game_type_id))
                continue
            
            for game in game_log_for_season_json['gameLog']:
                   
                    listing = [
                        game.get('gameId'),
                        game.get('teamAbbrev'),
                        game.get('homeRoadFlag'),
                        game.get('gameDate'),
                        season_id,
                        game.get('goals', 0),
                        game.get('assists', 0),
                        game.get('commonName.default', ''),
                        game.get('opponentCommonName.default', ''),
                        game.get('gamesStarted', 0),
                        game.get('decision', ''),
                        game.get('shotsAgainst', 0),
                        game.get('goalsAgainst', 0),
                        game.get('savePctg', 0.0),
                        game.get('shutouts', 0),
                        game.get('opponentAbbrev', ''),
                        game.get('pim', 0),
                        game.get('toi', '')
                    ]
                    skater_game_log_data.append(listing)
                    print(f"Added game log for skater {player_id}, season {season_id}, game type {game_type_id}")

print_game_logs_to_csv("skater_game_logs.csv", skater_column_headers, skater_game_log_data)
