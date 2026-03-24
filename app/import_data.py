import json
import sqlite3

from django import db

DB_PATH = 'sports_calendar.db'


def get_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sport")
    sports = cursor.fetchall()

    cursor.execute("SELECT * FROM team")
    teams = cursor.fetchall()


    conn.close()

    return {
        "sports": sports,
        "teams": teams,

    }


def import_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Import data into the database
    for match in data['sports']:
        comp_id = match.get('originCompetitionId')
        if comp_id:
            db.execute(
                "INSERT OR IGNORE INTO competition (id, name) VALUES (?, ?)",
                (comp_id, match.get('originCompetitionName'))
            )

        def upsert_team(team_data):
            if team_data is None:
                return None
            return get_data(
                db, 'team', 'slug', team_data['slug'],
                {
                    'name':          team_data['name'],
                    'official_name': team_data.get('officialName'),
                    'slug':          team_data['slug'],
                    'abbreviation':  team_data.get('abbreviation'),
                    'country_code':  team_data.get('teamCountryCode'),
                    '_sport_id':     sport_id,
                }
            )
        home_team_id = upsert_team(match.get('homeTeam'))
        away_team_id = upsert_team(match.get('awayTeam'))

        result     = match.get('result') or {}
        home_goals = result.get('homeGoals')
        away_goals = result.get('awayGoals')
        winner     = result.get('winner')

        
        db.execute(
            """
            INSERT INTO event (
                event_date, event_time, status, season,
                home_goals, away_goals, winner,
                _sport_id, _home_team_id, _away_team_id,
                _competition_id, _stage_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                match['dateVenue'],
                match['timeVenueUTC'],
                match.get('status'),
                match.get('season'),
                home_goals,
                away_goals,
                winner,
                sport_id,
                home_team_id,
                away_team_id,
                comp_id,
                stage_id,
            )
        )

    db.commit()
    db.close()
    print(f"Imported {len(data['data'])} matches.")


    conn.commit()
    conn.close()
