import sqlite3
import click
from flask import current_app, g

def init_db(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db_command():
    # Initializes the database 
        db = get_db()
        with current_app.open_resource('data.sql') as f:
            db.executescript(f.read().decode('utf8'))
        click.echo('Initialized the database.')

def get_db():
    # Opens a new database connection 
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    # Closes the database connection after each request
    db = g.pop('db', None)
    if db is not None:
        db.close()