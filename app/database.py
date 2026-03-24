import sqlite3
import click
from flask import current_app, g


def init_db(app):
    # register teardown and CLI commands
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)


@click.command('init-db')
def init_db_command():
    """CLI: flask init-db"""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    click.echo('Initialized the database.')


@click.command('seed-db')
def seed_db_command():
    """CLI: flask seed-db"""
    db = get_db()
    with current_app.open_resource('seed.sql') as f:
        db.executescript(f.read().decode('utf8'))
    click.echo('Database seeded.')


def get_db():
    # if connection doesn't exist, create a new one
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # return rows as dicts
    return g.db


def close_db(e=None):
    # close the connection after each request
    db = g.pop('db', None)
    if db is not None:
        db.close()