-- SQLite
CREATE TABLE Users (
    user_id CHAR(50) PRIMARY KEY,
    username CHAR(25) NOT NULL
);

CREATE TABLE Leagues (
    league_id CHAR(25) PRIMARY KEY,
    league_name CHAR(50) NOT NULL,
    total_rosters INTEGER NOT NULL,
    platform CHAR(10) NOT NULL,
    roster_positions CHAR(100) NOT NULL,
    season INTEGER NOT NULL,
    season_type CHAR(15) NOT NULL
)

CREATE TABLE UserLeague (
    user_id CHAR(25) NOT NULL,
    league_id CHAR(25) NOT NULL,
    PRIMARY KEY (user_id, league_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
    FOREIGN KEY(league_id) REFERENCES Leagues(league_id) 
)

-- SELECT * FROM Users;