# NHL-API-Games-to-CSV
This project uses the NHL API in a few ways in order to ultimately fetch game logs for active NHL player careers. Firstly, a for loop runs for each team tricode like (ANA for Anaheim), fetching the the current team rosters. It accesses the forwards, defense, and goalies. Combining forwards/defense into a skater's list, and keeping goalies as it's own list. Within those lists, it grabs the playerId, which is then used to access the individual player API, which returns seasonTotals, where you can get each season the player has played in the NHL. Once the player_id and respective seasons in the NHL are had, it's now possible to access each of their game_logs, which are fetched from the API, added to a data list, and at the final stop are imputted into a CSV file dependent on position.
# NHL API Scraper


## Scraping NHL Game Stats For Skaters & Goalies
## Scraping NHL Shifts
  GOAL: Retrieve data to provide context for shift length and how each player's shifts end
  PROCESS: 
    1. Call NHL shift chart, and play-by-play event api for a specific gameId
    2. Normalize naming data inside dataframes for more readable comparisons
    3. Get Play Stoppages
        a. Where typeDescKey == 'goal' or 'stoppages' stoppage_reason === details['reason']
        b. Where shiftChart['endTime'] == "20:00" --> stoppage_reason == "period-end"
    4. Determine how each shift ends
        a. Where period and time in period equal each other from both the stoppages & shifts = stoppages
        b. Set reasons for all null values to "other" as available NHL data does not specify reason for the shift ending
    5. Print to CSV
## Scraping NHL Events
## Scraping NHL Draft Picks
