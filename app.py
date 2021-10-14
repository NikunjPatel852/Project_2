import os
from numpy.core.fromnumeric import reshape
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

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/countrieslist")
def countrieslist():
    # Create our session (link) from Python to the DB
    session = Session(db.engine)

    """Return a list of all country names"""
    # Query all passengers
    list_countries= session.query(worlddata.rep_countries).distinct().all()
    list_countries.sort()
    session.close()

    # Convert list of tuples into normal list

    countries = [list_countries[0] for list_countries in list_countries]
    # countries = list(np.ravel(list_countries))
    # print(countries)
    return jsonify(countries)

@app.route("/api/v1.1/yearslist")
def yearslist():
    # Create our session (link) from Python to the DB
    session = Session(db.engine)

    """Return a list of all years"""
    # Query all years
    list_year= session.query(worlddata.year).distinct().all()
   
    print(list_year)
    session.close()

    # Convert list of tuples into normal list
    all_years = [x[0] for x in list_year]
    
    # all_years = list(np.ravel(list_year))
    results = { "years" : all_years}
    return jsonify(results)

if __name__ == "__main__":
    app.debug = False
    app.run()