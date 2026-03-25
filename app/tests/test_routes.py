import pytest
from app import create_app


#  Fixtures 
@pytest.fixture
def app():
    # Create app with in-memory test database.
    app = create_app({
        'TESTING': True,
        'DATABASE': ':memory:',
    })

    with app.app_context():
        from app.database import get_db
        db = get_db()

        with app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf-8'))

        db.executescript("""
            INSERT INTO sport (id, name) VALUES (1, 'Football');
            INSERT INTO sport (id, name) VALUES (2, 'Ice Hockey');

            INSERT INTO team (id, name, slug, _sport_id)
            VALUES (1, 'Salzburg', 'salzburg', 1);

            INSERT INTO team (id, name, slug, _sport_id)
            VALUES (2, 'Sturm', 'sturm', 1);

            INSERT INTO team (id, name, slug, _sport_id)
            VALUES (3, 'KAC', 'kac', 2);

            INSERT INTO team (id, name, slug, _sport_id)
            VALUES (4, 'Capitals', 'capitals', 2);

            INSERT INTO event (
                id, event_date, event_time, venue, status, season,
                home_goals, away_goals, winner,
                _sport_id, _home_team_id, _away_team_id
            ) VALUES (
                1, '2019-07-18', '18:30:00', 'Red Bull Arena',
                'played', 2019, 3, 1, 'Salzburg', 1, 1, 2
            );

            INSERT INTO event (
                id, event_date, event_time, status, season,
                _sport_id, _home_team_id, _away_team_id
            ) VALUES (
                2, '2019-10-23', '09:45:00', 'played', 2019, 2, 3, 4
            );
        """)

    yield app


@pytest.fixture
def client(app):
    # Test client for making requests.
    return app.test_client()


# GET /api/events 

def test_get_all_events_returns_200(client):
    # Returns 200 on success.
    response = client.get('/api/events')
    assert response.status_code == 200


def test_get_all_events_returns_list(client):
    # Returns list of events.
    response = client.get('/api/events')
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_all_events_contains_correct_fields(client):
    #Each event has required fields.
    response = client.get('/api/events')
    data = response.get_json()

    # just check the first event
    event = data[0]
    assert 'id' in event
    assert 'event_date' in event
    assert 'event_time' in event
    assert 'sport' in event
    assert 'home_team' in event
    assert 'away_team' in event


def test_get_events_filter_by_sport(client):
    #Filter by sport returns correct events.
    response = client.get('/api/events?sport=Football')
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['sport'] == 'Football'


def test_get_events_filter_by_date(client):
    # Filter by date returns correct events.
    response = client.get('/api/events?date=2019-07-18')
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['event_date'] == '2019-07-18'


def test_get_events_filter_no_results(client):
    # Filter with no matches returns empty list.
    response = client.get('/api/events?sport=Basketball')
    data = response.get_json()
    assert data == []


#GET /api/events/<id>

def test_get_single_event_returns_200(client):
    # Returns 200 for existing event.
    response = client.get('/api/events/1')
    assert response.status_code == 200


def test_get_single_event_returns_correct_data(client):
    # Returns correct event data.
    response = client.get('/api/events/1')
    data = response.get_json()

    # check all fields manually
    assert data['id'] == 1
    assert data['home_team'] == 'Salzburg'
    assert data['away_team'] == 'Sturm'
    assert data['sport'] == 'Football'
    assert data['event_date'] == '2019-07-18'
    assert data['home_goals'] == 3
    assert data['away_goals'] == 1
    assert data['winner'] == 'Salzburg'


def test_get_single_event_not_found(client):
    # Returns 404 for missing event.
    response = client.get('/api/events/999')
    assert response.status_code == 404


# POST /api/events

def test_add_event_returns_201(client):
    #Returns 201 on successful creation.
    response = client.post('/api/events', json={
        'event_date':    '2024-05-01',
        'event_time':    '20:00:00',
        'venue':         'Test Arena',
        'status':        'scheduled',
        'season':        2024,
        '_sport_id':     1,
        '_home_team_id': 1,
        '_away_team_id': 2,
    })
    assert response.status_code == 201


def test_add_event_returns_id(client):
    # Returns id of created event.
    response = client.post('/api/events', json={
        'event_date':    '2024-05-01',
        'event_time':    '20:00:00',
        '_sport_id':     1,
        '_home_team_id': 1,
        '_away_team_id': 2,
    })
    data = response.get_json()
    assert 'id' in data
    assert isinstance(data['id'], int)


def test_add_event_missing_fields_returns_400(client):
    # Returns 400 when required fields missing.
    response = client.post('/api/events', json={
        'event_date': '2024-05-01',
        # missing event_time, _sport_id, _home_team_id, _away_team_id
    })
    assert response.status_code == 400


def test_add_event_empty_body_returns_400(client):
    # Returns 400 for empty request body.
    response = client.post('/api/events', json={})
    assert response.status_code == 400


def test_add_event_appears_in_list(client):
    # New event is visible in GET /api/events.
    # first check how many events we have
    response_before = client.get('/api/events')
    count_before    = len(response_before.get_json())

    client.post('/api/events', json={
        'event_date':    '2024-06-01',
        'event_time':    '15:00:00',
        '_sport_id':     2,
        '_home_team_id': 3,
        '_away_team_id': 4,
    })

    response_after = client.get('/api/events')
    count_after    = len(response_after.get_json())

    # should be one more than before
    assert count_after == count_before + 1