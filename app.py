import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Data_Scrab/trade_world.db")

Base = automap_base()
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

#trade = Base.classes.worlddata

session = Session(engine)

#weather app
app = Flask(__name__)