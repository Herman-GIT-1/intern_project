from flask import Blueprint, jsonify, request, abort, render_template
from .database import get_db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    #Render all events as HTML.
    sport  = request.args.get('sport')
    date   = request.args.get('date')
    events = _fetch_all_events(sport=sport, date=date)
    return render_template('index.html', events=events)


@bp.route('/events/<int:event_id>')
def event_detail(event_id):
    #Render single event page.
    event = _fetch_event(event_id)
    if event is None:
        abort(404)
    return render_template('event.html', event=event)




@bp.route('/api/events', methods=['GET'])
def api_get_events():
   #Return all events as JSON.
    sport  = request.args.get('sport')
    date   = request.args.get('date')
    events = _fetch_all_events(sport=sport, date=date)
    return jsonify(events)


@bp.route('/api/events/<int:event_id>', methods=['GET'])
def api_get_event(event_id):
    """Return single event as JSON."""
    event = _fetch_event(event_id)
    if event is None:
        abort(404, description=f'Event with id {event_id} not found.')
    return jsonify(event)


@bp.route('/api/events', methods=['POST'])
def api_add_event():
    """Add new event to database."""
    data = request.get_json()

    required_fields = ('event_date', 'event_time',
                       '_sport_id', '_home_team_id', '_away_team_id')
    if not data or not all(field in data for field in required_fields):
        abort(400, description=f'Missing required fields: {required_fields}')

    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO event (
            event_date, event_time, venue, status, season,
            _sport_id, _home_team_id, _away_team_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data['event_date'],
            data['event_time'],
            data.get('venue'),
            data.get('status', 'scheduled'),
            data.get('season'),
            data['_sport_id'],
            data['_home_team_id'],
            data['_away_team_id'],
        )
    )
    db.commit()
    #print(f"Inserted event with ID: {cursor.lastrowid}")
    return jsonify({'id': cursor.lastrowid}), 201



def _fetch_all_events(sport=None, date=None):
    #Fetch all events with JOIN.
    query = """
        SELECT
            e.id,
            e.event_date,
            e.event_time,
            e.venue,
            e.status,
            e.season,
            e.home_goals,
            e.away_goals,
            e.winner,
            s.name  AS sport,
            ht.name AS home_team,
            at.name AS away_team
        FROM  event e
        JOIN      sport s  ON s.id  = e._sport_id
        LEFT JOIN team  ht ON ht.id = e._home_team_id
        LEFT JOIN team  at ON at.id = e._away_team_id
        WHERE 1=1
    """
    params = []

    if sport:
        query += " AND LOWER(s.name) = LOWER(?)"
        params.append(sport)

    if date:
        query += " AND e.event_date = ?"
        params.append(date)

    query += " ORDER BY e.event_date, e.event_time"

    rows = get_db().execute(query, params).fetchall()
    return [dict(row) for row in rows]


def _fetch_event(event_id):
    #Fetch one event by id.
    row = get_db().execute(
        """
        SELECT
            e.id,
            e.event_date,
            e.event_time,
            e.venue,
            e.status,
            e.season,
            e.home_goals,
            e.away_goals,
            e.winner,
            s.name  AS sport,
            ht.name AS home_team,
            at.name AS away_team
        FROM  event e
        JOIN      sport s  ON s.id  = e._sport_id
        LEFT JOIN team  ht ON ht.id = e._home_team_id
        LEFT JOIN team  at ON at.id = e._away_team_id
        WHERE e.id = ?
        """,
        (event_id,)
    ).fetchone()

    return dict(row) if row else None
