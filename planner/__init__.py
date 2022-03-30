import os
from flask import Flask, render_template, flash, session
from flask_session import Session
import psycopg2

from . import db

def create_app(test_config=None):
  app = Flask("planner")
  app.secretkey = "very_secret_key"
  app.config["SESSION_PERMANENT"] = False
  app.config["SESSION_TYPE"] = "filesystem"
  app.config.from_mapping(DATABASE = "plannerdata")
  Session(app)
  
  if (test_config is not None):
    app.config.update(test_config)
  
  try:
    os.makedirs(app.instance_path)
  
  except OSError:
    pass
    
  from . import plan
  app.register_blueprint(plan.bp)
  
  from . import db
  db.init_app(app)
  
  return app
