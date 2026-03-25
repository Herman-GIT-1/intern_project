# Sports Calendar

A simple web application for managing and displaying sports events.
Built with Flask and SQLite as part of the Sportradar Coding Academy exercise.

## Features

- View all sports events in a table with date, time, sport, teams, and result
- Filter events by sport or date
- View detailed information for a single event
- Add new events via form or REST API
- Import events from external JSON data

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, Jinja2 templates

## Project Structure
```
intern_project/
├── app/
│   ├── __init__.py       # app factory
│   ├── database.py       # db connection and CLI commands
│   ├── routes.py         # routes and API endpoints
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── event.html
│   └── static/
│       └── style.css
├── tests/
│   └── test_routes.py
├── schema.sql            # table definitions
├── seed.sql              # sample data
├── import_data.py        # import events from JSON
├── run.py                # entry point
├── requirements.txt
└── README.md
```

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/HERMAN-GIT-1/intern_project.git
cd intern_project
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Initialize the database**
```bash
flask --app run init-db
```

**5. Seed with sample data**
```bash
flask --app run seed-db
```

**6. Run the application**
```bash
python run.py
```

Open http://localhost:5000 in your browser.

## API Endpoints

| Method | Endpoint            | Description          |
|--------|---------------------|----------------------|
| GET    | `/api/events`       | Get all events       |
| GET    | `/api/events/<id>`  | Get single event     |
| POST   | `/api/events`       | Add new event        |

### Filters
```
GET /api/events?sport=Football
GET /api/events?date=2019-07-18
GET /api/events?sport=Football&date=2019-07-18
```

### POST /api/events

Request body:
```json
{
    "event_date":    "2024-05-01",
    "event_time":    "20:00:00",
    "venue":         "Red Bull Arena",
    "status":        "scheduled",
    "season":        2024,
    "_sport_id":     1,
    "_home_team_id": 1,
    "_away_team_id": 2
}
```

Response:
```json
{ "id": 7 }
```

## Import from JSON

To import events from an external JSON file:
```bash
python import_data.py
```

The file expects a JSON structure with a `data` array of match objects
(see `data.json` for format reference).

## Running Tests
```bash
pytest tests/ -v
```

Tests use an in-memory SQLite database so they don't affect real data.


## Requirements
```
flask
pytest
```