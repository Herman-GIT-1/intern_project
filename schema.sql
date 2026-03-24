CREATE TABLE sport (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE team (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    official_name TEXT,
    slug         TEXT UNIQUE,
    abbreviation TEXT,
    country_code TEXT,
    _sport_id    INTEGER NOT NULL,
    FOREIGN KEY (_sport_id) REFERENCES sport(id)
);

CREATE TABLE competition (
    id   TEXT PRIMARY KEY,   
    name TEXT NOT NULL
);

CREATE TABLE stage (
    id       TEXT PRIMARY KEY,  
    name     TEXT NOT NULL,
    ordering INTEGER
);

CREATE TABLE event (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    event_date    DATE    NOT NULL,
    event_time    TIME    NOT NULL,
    venue         TEXT,
    status        TEXT,           
    season        INTEGER,
    home_goals    INTEGER,
    away_goals    INTEGER,
    winner        TEXT,
    _sport_id     INTEGER NOT NULL,
    _home_team_id INTEGER,        
    _away_team_id INTEGER,
    _competition_id TEXT,
    _stage_id       TEXT,
    FOREIGN KEY (_sport_id)       REFERENCES sport(id),
    FOREIGN KEY (_home_team_id)   REFERENCES team(id),
    FOREIGN KEY (_away_team_id)   REFERENCES team(id),
    FOREIGN KEY (_competition_id) REFERENCES competition(id),
    FOREIGN KEY (_stage_id)       REFERENCES stage(id)
);