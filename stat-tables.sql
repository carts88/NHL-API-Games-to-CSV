CREATE TABLE IF NOT EXISTS skater_events (
    game_id BIGINT,
    event_type ENUM('goal', 'assist', 'penalty', 'shot', 'hit', 'block'),
    player_id BIGINT,
    period INT,
    time_remaining 
)


CREATE TABLE IF NOT EXISTS bios (
    player_id BIGINT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    height_in_inches INT,
    weight_in_pounds INT,
    default_position ENUM('C', 'LW', 'RW', 'LD', 'RD', 'D', 'G') NOT NULL,
    shoots_catches ENUM('L', 'R') NOT NULL,
    current_team_tricode VARCHAR(3),
    country VARCHAR(50) NOT NULL,
    city_province VARCHAR(50) NOT NULL,
    amateur_league VARCHAR(50) NOT NULL,
    amateur_team VARCHAR(50) NOT NULL,
)


CREATE TABLE IF NOT EXISTS drafts (
    draft_pick_id VARCHAR(255) PRIMARY KEY,
    current_owner VARCHAR(3) NOT NULL,
    original_owner VARCHAR(3) NOT NULL,
    draft_year INT NOT NULL,
    draft_round INT NOT NULL,
    draft_overall INT NOT NULL,
    player_id BIGINT NOT NULL,
    team_tricode VARCHAR(3) NOT NULL,
)


CREATE TABLE IF NOT EXISTS shot_locations (
    player_id BIGINT PRIMARY KEY,
    game_id BIGINT NOT NULL,
    shot_id BIGINT NOT NULL,
    x_coordinate FLOAT NOT NULL,
    y_coordinate FLOAT NOT NULL,
    shot_type ENUM('wrist', 'slap', 'snap', 'backhand') NOT NULL,
    shot_result ENUM('blocked-shot', 'shot-on-goal', 'slap', 'snap') NOT NULL
    shooting_player_id
    blocking_player_id
    opposing_goalie_id
);


CREATE TABLE IF NOT EXISTS skater_game_logs (
    player_id BIGINT NOT NULL,
    game_id BIGINT NOT NULL,
    season VARCHAR(10) NOT NULL,
    toi VARCHAR(15) NOT NULL,
    shots INT NOT NULL DEFAULT 0,
    hits INT NOT NULL DEFAULT 0,
    blocks INT NOT NULL DEFAULT 0,
    goals INT NOT NULL DEFAULT 0,
    primary_assists INT NOT NULL DEFAULT 0
    secondary_assists INT NOT NULL DEFAULT 0,
    penalties_taken INT NOT NULL DEFAULT 0,
    penalty_minutes VARCHAR(15) NOT NULL,
);



CREATE TABLE IF NOT EXISTS events (
    event_id BIGINT PRIMARY KEY,
    game_id BIGINT FOREIGN KEY
    period ENUM(1,2,3)
    secondsRemaining INT NOT NULL,
    event_type
    situation_code  
    homeTeamDefendingSide
    utc DATE 
)


CREATE TABLE IF NOT EXISTS penalties (
    event_id BIGINT FOREIGN KEY
    x_coordinate INT NOT NULL
    y_coordinate INT NOT NULL
    zone_code ENUM('O', 'D', 'N')
    penalty_type
    drawn_by_player_id BIGINT FOREIGN KEY
    committed_by_player_ud BIGINT FOREIGN KEY
)

CREATE TABLE IF NOT EXISTS penalties (
    event_id BIGINT FOREIGN KEY
    x_coordinate INT NOT NULL
    y_coordinate INT NOT NULL
    zone_code ENUM('O', 'D', 'N')
    penalty_type
    drawn_by_player_id BIGINT FOREIGN KEY
    committed_by_player_ud BIGINT FOREIGN KEY
)


CREATE TABLE IF NOT EXISTS hit_locations (
    event_id
    hitting_player_id
    hittee_player_id
)







CREATE TABLE IF NOT EXISTS staff_bios (
    staff_id int PRIMARY KEY
    player_id INT
    first_name TEXT NOT NULL
    last_name TEXT NOT NULL
    nhl_bio TEXT
    birthdate DATE NOT NULL
    date_of_death DATE
    birth_city VARCHAR(100)
    birth_country_code VARCHAR(50)
    nationality_code VARCHAR(50)
    birth_state_province_code VARCHAR(50)
)

CREATE TABLE IF NOT EXISTS nhl_games (
    game_id BIGINT PRIMARY KEY,
    game_date DATE,
    home_team VARCHAR
    home_score INT
    away_team VARCHAR
    away_score INT
)


CREATE TABLE IF NOT EXISTS nhl_shifts (
    game_id BIGINT PRIMARY KEY,
    player_id INT FOREIGN KEY
    shift_number INT
    shift_duration
    shift_start_time
    shift_end_time
    detail_code
    event_description
)

