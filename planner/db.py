import os
import psycopg2
import datetime
from flask import g, current_app, flash
from flask.cli import with_appcontext
import click
import sqlite3

def get_db():
  if 'db' not in g:
    dbname = current_app.config['DATABASE']
    g.db = psycopg2.connect(f'dbname = {dbname}')
  return g.db
  
def close_db(e=None):
  db = g.pop('db', None)
  if db is not None:
    db.close()
    
def init_db():
  db = get_db()
  f = current_app.open_resource('sql/setup_db.sql')
  sql_code = f.read().decode('ascii')
  
  p = db.cursor()
  p.execute(sql_code)
  p.close()
  db.commit()
  close_db()
  
@click.command('initdb', help = 'Initialises the Database')
@with_appcontext
def init_db_command():
  init_db()
  click.echo('Database "plannerdata" has been initialised')
  
def init_app(app):
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)
  
