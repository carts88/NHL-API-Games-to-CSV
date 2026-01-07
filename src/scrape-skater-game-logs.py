import pandas as pd

import requests
import csv

""""
PLAN: Access base NHL player API https://api-web.nhle.com/v1/player/{player_id}, access seasonTotals.season if exists. If that season exists fetch game logs for that season, and imput them into player_game_logs.csv, once done fetching data for that player then fetch re-run same process for another player
"""

team_codes = ['ANA', 'ARI', 'BOS', 'BUF', 'CGY', 'CHI', 'COL', 'CBJ', 'DAL', 'DET', 'EDM', 'FLA', 'LAK', 'MIN', 'MTL', 'NJD', 'NSH', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'SJS', 'STL', 'TBL', 'TOR', 'VAN', 'VGK', 'WPG', 'UTA']

# roster_api_season = 20242025

# skater_column_headers = [
#     'game_id', 'team_tricode', 'season', 'home_road_flag', 'goals', 'assists', 'team_nickname',
#     'opponent_nickname','points','plus_minus','power_play_goals','power_play_points','game_winning_goals',
#     'ot_goals', 'shots', 'shifts', 'shorthanded_goals', 'shorthanded_points', 'opponent_tricode','pim', 'toi'
# ]

# goalie_column_headers = [
#     'game_id',
#     'team_tricode',       # from teamAbbrev
#     'home_road_flag',
#     'date',               # from gameDate
#     'season',             # if you include it as before
#     'goals',
#     'assists',
#     'common_name',
#     'opponent_common_name',
#     'games_started',
#     'decision',
#     'shots_against',
#     'goals_against',
#     'save_pctg',
#     'shutouts',
#     'opponent_abbrev',
#     'pim',
#     'toi'
# ]

# def get_player_game_log_url(player_id: int, season_id: int, game_type_id: int):
#     return f"{api_base_url}/player/{player_id}/game-log/{season_id}/{game_type_id}"

# def print_game_logs_to_csv(csvFileName: str, column_headers: list[str], game_logs: list[dict]):
#     with open(csvFileName, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(column_headers)  # Header
#         writer.writerows(game_logs)


# # configuration values
# skater_id_list = []
# goalie_id_list = []
# game_type_ids = [ 2, 3]

# # initial empty data lists
# skater_game_log_data = []
# goalie_game_log_data = []
# players_not_found = []
# game_logs_not_found = []


# # first loop to get all player IDs from rosters
# for tricode in team_codes: 
#     roster_api_url = f"{api_base_url}/roster/{tricode}/{roster_api_season}"
#     roster_api_response = requests.get(roster_api_url)

#     if roster_api_response.status_code != 200:
#         print(f"Error fetching roster for {tricode}: {roster_api_response.status_code}")
#         continue
#     roster_data = roster_api_response.json()
    
#     for forward in roster_data.get('forwards', []):
#         skater_id_list.append(forward['id'])
#     for defenseman in roster_data.get('defensemen', []):
#         skater_id_list.append(defenseman['id'])
#     for goalie in roster_data.get('goalies', []):
#         goalie_id_list.append(goalie['id'])
    


# # big boy loop for goalies
# for player_id in goalie_id_list:
#     player_api_url = f"{api_base_url}/player/{player_id}/landing"
#     player_api_response = requests.get(player_api_url)
    
#     # If there is no response for that Player ID then it prints an error, and adds the playerId to a list, as well as skipping the rest of the iteration
#     if player_api_response.status_code != 200:
#         print(f"Error fetching data for player {player_id}: {player_api_response.status_code}")
#         players_not_found.append(player_id) 
#         continue
    
#     player_data = player_api_response.json()
    
#     season_ids = [
#         season['season']
#         for season in player_data.get('seasonTotals', [])
#         if season.get('leagueAbbrev') == 'NHL'  # common key based on NHL API patterns
#     ]
        
#     for season_id in season_ids:
#         for game_type_id in game_type_ids:
#             game_log_for_season_api_url = get_player_game_log_url(player_id, season_id, game_type_id)
#             game_log_for_season_response = requests.get(game_log_for_season_api_url)
#             game_log_for_season_json = game_log_for_season_response.json()
            
#             if 'gameLog' not in game_log_for_season_json:
#                 print(f"No gameLog data for player {player_id}, season {season_id}, game type {game_type_id}")
#                 game_logs_not_found.append((player_id, season_id, game_type_id))
#                 continue
            
#             for game in game_log_for_season_json['gameLog']:
#                     listing = [
#                         game.get('gameId'),
#                         game.get('teamAbbrev'),
#                         game.get('homeRoadFlag'),
#                         game.get('gameDate'),
#                         season_id,
#                         game.get('goals', 0),
#                         game.get('assists', 0),
#                         game.get('commonName.default', ''),
#                         game.get('opponentCommonName.default', ''),
#                         game.get('gamesStarted', 0),
#                         game.get('decision', ''),
#                         game.get('shotsAgainst', 0),
#                         game.get('goalsAgainst', 0),
#                         game.get('savePctg', 0.0),
#                         game.get('shutouts', 0),
#                         game.get('opponentAbbrev', ''),
#                         game.get('pim', 0),
#                         game.get('toi', '')
#                     ]
#                     goalie_game_log_data.append(listing)
#                     print(f"Added game log for goalie {player_id}, season {season_id}, game type {game_type_id}")
                    
                    
                    
# print_game_logs_to_csv("goalie_game_logs.csv", goalie_column_headers, goalie_game_log_data)


# # big boy loop for skaters
# for player_id in skater_id_list:
#     player_api_url = f"{api_base_url}/player/{player_id}/landing"
#     player_api_response = requests.get(player_api_url)
    
#     # If there is no response for that Player ID then it prints an error, and adds the playerId to a list, as well as skipping the rest of the iteration
#     if player_api_response.status_code != 200:
#         print(f"Error fetching data for player {player_id}: {player_api_response.status_code}")
#         players_not_found.append(player_id) 
#         continue
    
#     player_data = player_api_response.json()
    
#     season_ids = [
#         season['season']  
#         for season in player_data.get('seasonTotals', [])
#         if season.get('leagueAbbrev') == 'NHL' 
#     ]
    
#     for season_id in season_ids:
#         for game_type_id in game_type_ids:
#             game_log_for_season_api_url = get_player_game_log_url(player_id, season_id, game_type_id)
#             game_log_for_season_response = requests.get(game_log_for_season_api_url)
#             game_log_for_season_json = game_log_for_season_response.json()
            
#             if 'gameLog' not in game_log_for_season_json:
#                 print(f"No gameLog data for player {player_id}, season {season_id}, game type {game_type_id}")
#                 game_logs_not_found.append((player_id, season_id, game_type_id))
#                 continue
            
#             for game in game_log_for_season_json['gameLog']:
                   
#                     listing = [
#                         game.get('gameId'),
#                         game.get('teamAbbrev'),
#                         game.get('homeRoadFlag'),
#                         game.get('gameDate'),
#                         season_id,
#                         game.get('goals', 0),
#                         game.get('assists', 0),
#                         game.get('commonName.default', ''),
#                         game.get('opponentCommonName.default', ''),
#                         game.get('gamesStarted', 0),
#                         game.get('decision', ''),
#                         game.get('shotsAgainst', 0),
#                         game.get('goalsAgainst', 0),
#                         game.get('savePctg', 0.0),
#                         game.get('shutouts', 0),
#                         game.get('opponentAbbrev', ''),
#                         game.get('pim', 0),
#                         game.get('toi', '')
#                     ]
#                     skater_game_log_data.append(listing)
#                     print(f"Added game log for skater {player_id}, season {season_id}, game type {game_type_id}")

# print_game_logs_to_csv("skater_game_logs.csv", skater_column_headers, skater_game_log_data)


def get_player_ids_for_team(teams, seasons):
    print("User Inputted Parameters")
    print("teams: ", teams)
    print("\nFetching player_id for teams....\n")
    
    for team, season in teams, seasons: 
        roster_api_url = f"https://api-web.nhle.com/v1/roster/{team}/{season}"
        roster_api_response = requests.get(roster_api_url)

        if roster_api_response.status_code != 200:
            print(f"Error fetching roster for {teams}: {roster_api_response.status_code}")
            
        roster_data = roster_api_response.json()
        
        # for forward in roster_data.get('forwards', []):
        #     skater_id_list.append(forward['id'])
        # for defenseman in roster_data.get('defensemen', []):
        #     skater_id_list.append(defenseman['id'])
        # for goalie in roster_data.get('goalies', []):
        #     goalie_id_list.append(goalie['id'])


import pandas as pd
import requests

def get_player_ids_for_team(teams, seasons):
    print("User Inputted Parameters")
    print("teams: ", teams)
    print("seasons: ", seasons)
    print("\nFetching player_ids for teams....\n")
    
    # Initialize empty lists to collect all IDs across teams and seasons
    skater_ids_list = []
    goalie_ids_list = []
    
    for season in seasons:
        for team in teams: 
            roster_api_url = f"https://api-web.nhle.com/v1/roster/{team}/{season}"
            roster_api_response = requests.get(roster_api_url)
            
            if roster_api_response.status_code != 200:
                print(f"Error fetching roster for {team} in {season}: {roster_api_response.status_code}")
                continue
    
            roster = roster_api_response.json()
            
            # Extract forwards and defensemen (skaters)
            if 'forwards' in roster and roster['forwards']:
                df_forwards = pd.DataFrame(roster['forwards'], columns=['id'])
                skater_ids_list.append(df_forwards)
            
            if 'defensemen' in roster and roster['defensemen']:
                df_defense = pd.DataFrame(roster['defensemen'], columns=['id'])
                skater_ids_list.append(df_defense)
            
            # Extract goalies (fixed the bug here!)
            if 'goalies' in roster and roster['goalies']:
                df_goalies = pd.DataFrame(roster['goalies'], columns=['id'])
                goalie_ids_list.append(df_goalies)
    
    # Combine all skater IDs and remove duplicates
    if skater_ids_list:
        df_skater_ids = pd.concat(skater_ids_list, ignore_index=True)
        df_skater_ids = df_skater_ids.drop_duplicates(subset=['id']).reset_index(drop=True)
    else:
        df_skater_ids = pd.DataFrame(columns=['id'])
    
    # Combine all goalie IDs and remove duplicates
    if goalie_ids_list:
        df_goalie_ids = pd.concat(goalie_ids_list, ignore_index=True)
        df_goalie_ids = df_goalie_ids.drop_duplicates(subset=['id']).reset_index(drop=True)
    else:
        df_goalie_ids = pd.DataFrame(columns=['id'])
    
    print(f"Found {len(df_skater_ids)} unique skaters")
    print(f"Found {len(df_goalie_ids)} unique goalies")
    
    return df_skater_ids, df_goalie_ids

def get_seasons_in_nhl_for_player_id(player_id):
    """
    PARAMS: 
        player_id = equals NHL assigned id, used in order to fetch player specific api
    DESCRIPTION:
        This function takes in the player_id, in order to fetch the player api, then access 
        season totals to get the unique season_ids a player has participated in the nhl
    """
    player_api_url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    player_api_response = requests.get(player_api_url)

    if player_api_response.status_code != 200:
        print(f"Error fetching data for player {player_id}: {player_api_response.status_code}")
        return player_api_response.status_code
        
    
    player_data = player_api_response.json()
    df_nhl_seasons = pd.DataFrame(player_data['seasonTotals'], columns=['season', 'leagueAbbrev'])
    df_nhl_seasons = df_nhl_seasons[df_nhl_seasons['leagueAbbrev'] == "NHL"]
    unique_seasons = sorted(df_nhl_seasons['season'].unique())

    return unique_seasons
    
    
def get_skater_game_logs_for_season(seasons):
    print("User Inputted Parameters")
    print("Seasons: ", seasons)
    print("\nFetching player game logs....\n")
    
    # skater_game_log_api = f"{api_base_url}/player/{player_id}/game-log/{season_id}/{game_type_id}"

    
    


seasonss = get_seasons_in_nhl_for_player_id(8478402)




get_player_ids_for_team(['ANA', 'PHI'], [20242025])