import os
import pandas as pd
import json
import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import create_engine, distinct
from sqlalchemy.sql import func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from config import ServerName, UserName, Password, DataBase

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','') or f"postgres://{UserName}:{Password}@localhost:5432/{DataBase}"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
worlddata = Base.classes.worlddata

# @app.route("/")
# def index():
#     """Return the homepage."""
#     return render_template("index.html")

@app.route("/api/v1.0/names")
def names():
    # Create our session (link) from Python to the DB
    session = Session(db.engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(worlddata.year).all()

    session.close()

    # Convert list of tuples into normal list
    all_year = list(np.ravel(results))
    #print(all_year)
    return jsonify(all_year)

if __name__ == "__main__":
    app.debug = False
    app.run()