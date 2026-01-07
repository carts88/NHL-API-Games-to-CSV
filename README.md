# NHL API Scraper

A comprehensive tool for scraping and analyzing NHL player statistics, game logs, shifts, events, and draft data using the official NHL API.

## Features

### Game Logs
Automatically fetches complete career game logs for all active NHL players by:
- Iterating through each NHL team using their tricode identifiers (e.g., ANA for Anaheim)
- Retrieving current rosters including forwards, defensemen, and goalies
- Accessing individual player profiles via playerId
- Collecting seasonTotals data for each player's NHL career
- Compiling game logs and exporting to position-specific CSV files

### Shift Analysis
Retrieves detailed shift data to analyze shift length patterns and how shifts conclude.

**Process:**
1. Calls NHL shift chart and play-by-play event APIs for specific games
2. Normalizes naming conventions across dataframes for easier comparison
3. Identifies play stoppages:
   - Goals and general stoppages from event details
   - Period endings (when shift endTime equals "20:00")
4. Determines shift endings by:
   - Matching period and time-in-period between stoppages and shift data
   - Labeling unmatched shifts as "other" (when NHL data doesn't specify the reason)
5. Exports results to CSV

### Event Tracking
Scrapes play-by-play event data from NHL games.

### Draft Pick Data
Collects historical NHL draft pick information.

---

*All data sourced from the official NHL API*
