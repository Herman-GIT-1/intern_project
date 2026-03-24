import json
import sqlite3



DB_PATH = 'sports_calendar.db'


def get_or_create(cursor, table, lookup_field, lookup_value, insert_data):
    # Find or create a record and return its id.
    cursor.execute(
        f"SELECT id FROM {table} WHERE {lookup_field} = ?",
        (lookup_value,)
    )
    row = cursor.fetchone()
    if row:
        return row[0]

    cursor.execute(
        f"INSERT INTO {table} ({', '.join(insert_data.keys())}) "
        f"VALUES ({', '.join(['?'] * len(insert_data))})",
        list(insert_data.values())
    )
    return cursor.lastrowid


def import_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    sport_id = get_or_create(
        cursor, 'sport', 'name', 'Football', {'name': 'Football'}
    )

    for match in data['data']:  

        # Competition
        comp_id = match.get('originCompetitionId')
        if comp_id:
            cursor.execute(  
                "INSERT OR IGNORE INTO competition (id, name) VALUES (?, ?)",
                (comp_id, match.get('originCompetitionName'))
            )

        # Stage
        stage = match.get('stage')
        stage_id = None
        if stage:
            stage_id = stage['id']
            cursor.execute(
                "INSERT OR IGNORE INTO stage (id, name, ordering) VALUES (?, ?, ?)",
                (stage_id, stage['name'], stage['ordering'])
            )

        # Teams 
        def upsert_team(team_data):
            if team_data is None:
                return None
            return get_or_create( 
                cursor, 'team', 'slug', team_data['slug'],
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

        # Results
        result     = match.get('result') or {}
        home_goals = result.get('homeGoals')
        away_goals = result.get('awayGoals')
        winner     = result.get('winner')

        cursor.execute(  
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

    conn.commit()  
    conn.close()
    print(f"Imported {len(data['data'])} matches.")


if __name__ == '__main__':
    import_data('data.json')