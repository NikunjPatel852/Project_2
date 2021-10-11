# import
from flask.globals import session
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# reference to the table
#country = Base.


# Flask Setup
app = Flask(__name__)


# when a user clicks the index route
@app.route("/")
def home():
    return (
        f"This is the home page"
    )

# if user wants to select a country
@app.route("/dashboard/country/<country_name>")
def country(country_name):

    # session (link) from python to db
    session = Session(engine)



    session.close()

if __name__ == "__main__":
    app.run(debug=True)
