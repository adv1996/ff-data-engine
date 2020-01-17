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

CREATE TABLE Leagues (
    league_id CHAR(25) PRIMARY KEY,
    league_name CHAR(50) NOT NULL,
    total_rosters INTEGER NOT NULL,
    platform CHAR(10) NOT NULL,
    season INTEGER NOT NULL,
    season_type CHAR(15) NOT NULL,
    QB INTEGER NOT NULL,
    RB INTEGER NOT NULL,
    WR INTEGER NOT NULL,
    TE INTEGER NOT NULL,
    FLEX INTEGER NOT NULL,
    SUPER_FLEX INTEGER NOT NULL,
    DEF INTEGER NOT NULL,
    K INTEGER NOT NULL,
    BN INTEGER NOT NULL,
    REC_FLEX INTEGER NOT NULL,
    DL INTEGER NOT NULL,
    WRRB_FLEX INTEGER NOT NULL, 
    DB INTEGER NOT NULL,
    LB INTEGER NOT NULL,
    IDP_FLEX INTEGER NOT NULL,
)

CREATE TABLE UserLeague (
    user_id CHAR(25) NOT NULL,
    league_id CHAR(25) NOT NULL,
    roster_id INTEGER NOT NULL,
    wins INTEGER NOT NULL,
    ties INTEGER NOT NULL,
    fpts INTEGER NOT NULL,
    losses INTEGER NOT NULL,
    fpts_against INTEGER NOT NULL,
    PRIMARY KEY (user_id, league_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
    FOREIGN KEY(league_id) REFERENCES Leagues(league_id) 
)