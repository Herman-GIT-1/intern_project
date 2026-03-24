-- Sports
INSERT INTO sport (name) VALUES ('Football');
INSERT INTO sport (name) VALUES ('Ice Hockey');
INSERT INTO sport (name) VALUES ('Basketball');

-- Teams (Football)
INSERT INTO team (name, official_name, slug, abbreviation, country_code, _sport_id)
VALUES ('Salzburg', 'FC Red Bull Salzburg', 'fc-red-bull-salzburg', 'SAL', 'AUT', 1);

INSERT INTO team (name, official_name, slug, abbreviation, country_code, _sport_id)
VALUES ('Sturm', 'SK Sturm Graz', 'sk-sturm-graz', 'STU', 'AUT', 1);

INSERT INTO team (name, official_name, slug, abbreviation, country_code, _sport_id)
VALUES ('Al Hilal', 'Al Hilal Saudi FC', 'al-hilal-saudi-fc', 'HIL', 'KSA', 1);

INSERT INTO team (name, official_name, slug, abbreviation, country_code, _sport_id)
VALUES ('Nasaf', 'FC Nasaf', 'fc-nasaf-qarshi', 'NAS', 'UZB', 1);

-- Teams (Ice Hockey)
INSERT INTO team (name, official_name, slug, abbreviation, country_code, _sport_id)
VALUES ('KAC', 'EC KAC Klagenfurt', 'ec-kac-klagenfurt', 'KAC', 'AUT', 2);

INSERT INTO team (name, official_name, slug, abbreviation, country_code, _sport_id)
VALUES ('Capitals', 'Vienna Capitals', 'vienna-capitals', 'CAP', 'AUT', 2);

-- Teams (Basketball)
INSERT INTO team (name, official_name, slug, abbreviation, country_code, _sport_id)
VALUES ('Lakers', 'Los Angeles Lakers', 'la-lakers', 'LAL', 'USA', 3);

INSERT INTO team (name, official_name, slug, abbreviation, country_code, _sport_id)
VALUES ('Bulls', 'Chicago Bulls', 'chicago-bulls', 'CHI', 'USA', 3);

-- Competitions
INSERT INTO competition (id, name) VALUES ('austrian-bundesliga',  'Austrian Bundesliga');
INSERT INTO competition (id, name) VALUES ('austrian-hockey-league','Austrian Hockey League');
INSERT INTO competition (id, name) VALUES ('nba',                  'NBA');
INSERT INTO competition (id, name) VALUES ('afc-champions-league', 'AFC Champions League');

-- Stages
INSERT INTO stage (id, name, ordering) VALUES ('REGULAR SEASON', 'Regular Season', 1);
INSERT INTO stage (id, name, ordering) VALUES ('ROUND OF 16',    'Round of 16',    4);
INSERT INTO stage (id, name, ordering) VALUES ('FINAL',          'Final',          7);

-- Events (from task examples)
INSERT INTO event (event_date, event_time, venue, status, season,
                   home_goals, away_goals, winner,
                   _sport_id, _home_team_id, _away_team_id,
                   _competition_id, _stage_id)
VALUES ('2019-07-18', '18:30:00', 'Red Bull Arena', 'played', 2019,
        3, 1, 'Salzburg', 1, 1, 2, 'austrian-bundesliga', 'REGULAR SEASON');

INSERT INTO event (event_date, event_time, venue, status, season,
                   home_goals, away_goals, winner,
                   _sport_id, _home_team_id, _away_team_id,
                   _competition_id, _stage_id)
VALUES ('2019-10-23', '09:45:00', 'Stadthalle Klagenfurt', 'played', 2019,
        2, 4, 'Capitals', 2, 5, 6, 'austrian-hockey-league', 'REGULAR SEASON');

--Events (from AFC Champions League JSON)
INSERT INTO event (event_date, event_time, status, season,
                   home_goals, away_goals, winner,
                   _sport_id, _home_team_id, _away_team_id,
                   _competition_id, _stage_id)
VALUES ('2024-01-03', '00:00:00', 'played', 2024,
        1, 2, 'Nasaf', 1, 3, 4, 'afc-champions-league', 'ROUND OF 16');

INSERT INTO event (event_date, event_time, status, season,
                   _sport_id, _home_team_id, _away_team_id,
                   _competition_id, _stage_id)
VALUES ('2024-01-03', '16:00:00', 'scheduled', 2024,
        1, 3, 4, 'afc-champions-league', 'ROUND OF 16');


INSERT INTO event (event_date, event_time, status, season,
                   _sport_id, _home_team_id, _away_team_id,
                   _competition_id, _stage_id)
VALUES ('2024-01-19', '00:00:00', 'scheduled', 2024,
        1, NULL, 4, 'afc-champions-league', 'FINAL');


INSERT INTO event (event_date, event_time, venue, status, season,
                   _sport_id, _home_team_id, _away_team_id,
                   _competition_id, _stage_id)
VALUES ('2024-03-15', '20:00:00', 'United Center', 'scheduled', 2024,
        3, 7, 8, 'nba', 'REGULAR SEASON');