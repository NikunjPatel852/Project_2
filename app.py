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
from config import ServerName, UserName, Password, port, DataBase

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','') or f"postgresql://{UserName}:{Password}@localhost:5432/{DataBase}"
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
    results = countries
    # countries = list(np.ravel(list_countries))
    # print(results)
    return jsonify(results)


# for the country
@app.route("/<country>/stats")
def countryStats(country):
    print(country)
    export_rs = db.session.execute(""" 
    select sum(value) as value2, year
    from worlddata 
    where rep_countries = :country and element = 'Export Value'
    group by year
    """, {"country":country})
    export_stats = []
    for stat in export_rs:
        export_stats.append({
            "value": stat["value2"],
            "year": stat["year"]
        })
    return jsonify(export_stats)

@app.route("/importvaluedata")
def import2011data():
    # Create our session (link) from Python to the DB
    session = Session(db.engine)

    """Return a list of all country names"""
    # Query all passengers
    import_data = session.query(
        worlddata.rep_countries, 
        worlddata.par_countries, 
        worlddata.year, 
        worlddata.element, 
        worlddata.value, 
        worlddata.item).filter_by(element= 'Import Value').limit(10000).all()

    importV= pd.DataFrame(import_data, columns=[
        'rep_countries', 
        'par_countries', 
        'year',
        'element', 
        'value', 
        'item'])
    
    importV.sort_values('value',ascending=False).groupby(['rep_countries', 'item'])['value'].sum()
    importV.columns.get_level_values(0)
    importV.columns.to_flat_index()
    importV.columns = ['_'.join(x) for x in importV.columns.to_flat_index()]
    
    importV2 =importV.rename(columns= {
        'r_e_p___c_o_u_n_t_r_i_e_s': 'rep_countries',
        'p_a_r___c_o_u_n_t_r_i_e_s': 'par_countries',
        'y_e_a_r': 'year',
        'e_l_e_m_e_n_t': 'element',
        'v_a_l_u_e': 'value',
        'i_t_e_m': 'item'})
    
    importV3 = importV2.sort_values('value',ascending=False).reset_index()
    #importV3.head()
    importV4 = importV3.drop(columns=['element','index'])
    importV4 = importV4[importV4.value !=0]
    #importV4.head(50)
    importV5 = importV4.to_json(orient='records')
    
    return importV5

@app.route("/importquanitydata")
def importquantdata():
    # Create our session (link) from Python to the DB
    session = Session(db.engine)

    """Return a list of all country names"""
    # Query all passengers
    importv = session.query(
        worlddata.rep_countries, 
        worlddata.par_countries, 
        worlddata.year, 
        worlddata.element, 
        worlddata.value, 
        worlddata.item).filter_by(
            element= 'Import Quantity').limit(1000).all()

    importV= pd.DataFrame(importv, columns=[
        'rep_countries', 
        'par_countries', 
        'year',
        'element', 
        'value', 
        'item'])
    
    importV.sort_values('value',ascending=False).groupby(['rep_countries', 'item'])['value'].sum()
    importV.columns.get_level_values(0)
    importV.columns.to_flat_index()
    importV.columns = ['_'.join(x) for x in importV.columns.to_flat_index()]
    importV2 =importV.rename(columns= {
        'r_e_p___c_o_u_n_t_r_i_e_s': 'rep_countries',
        'p_a_r___c_o_u_n_t_r_i_e_s': 'par_countries',
        'y_e_a_r': 'year',
        'e_l_e_m_e_n_t': 'element',
        'v_a_l_u_e': 'value',
        'i_t_e_m': 'item'})
    
    importV3 = importV2.sort_values('value',ascending=False).reset_index()
    #exportV3.head()
    importV4 = importV3.drop(columns=['element','index', 'year'])
    #exportV4.head(50)
    importV5 = importV4.to_json(orient='records')
    
    return importV5

@app.route("/exportvaluedata")
def exportvaldata():
    # Create our session (link) from Python to the DB
    session = Session(db.engine)

    """Return a list of all country names"""
    # Query all passengers
    exportv = session.query(
        worlddata.rep_countries, 
        worlddata.par_countries, 
        worlddata.year, 
        worlddata.element, 
        worlddata.value, 
        worlddata.item).filter_by(
            element= 'Export Value', year = 2012).limit(1000).all()

    exportV= pd.DataFrame(exportv, columns=[
        'rep_countries', 
        'par_countries', 
        'year',
        'element', 
        'value', 
        'item'])
    
    exportV.sort_values('value',ascending=False).groupby(['rep_countries', 'item'])['value'].sum()
    exportV.columns.get_level_values(0)
    exportV.columns.to_flat_index()
    exportV.columns = ['_'.join(x) for x in exportV.columns.to_flat_index()]
    exportV2 =exportV.rename(columns= {
        'r_e_p___c_o_u_n_t_r_i_e_s': 'rep_countries',
        'p_a_r___c_o_u_n_t_r_i_e_s': 'par_countries',
        'y_e_a_r': 'year',
        'e_l_e_m_e_n_t': 'element',
        'v_a_l_u_e': 'value',
        'i_t_e_m': 'item'})
    
    exportV3 = exportV2.sort_values('value',ascending=False).reset_index()
    #exportV3.head()
    exportV4 = exportV3.drop(columns=['element','index', 'year'])
    #exportV4.head(50)
    exportV5 = exportV4.to_json(orient='records')
    
    return exportV5

@app.route("/exportquanitydata")
def exportquantdata():
    # Create our session (link) from Python to the DB
    session = Session(db.engine)

    """Return a list of all country names"""
    # Query all passengers
    exportv = session.query(
        worlddata.rep_countries, 
        worlddata.par_countries, 
        worlddata.year, 
        worlddata.element, 
        worlddata.value, 
        worlddata.item).filter_by(
            element= 'Export Value', year = 2011).limit(1000).all()

    exportV= pd.DataFrame(exportv, columns=[
        'rep_countries', 
        'par_countries', 
        'year',
        'element', 
        'value', 
        'item'])
    
    exportV.sort_values('value',ascending=False).groupby(['rep_countries', 'item'])['value'].sum()
    exportV.columns.get_level_values(0)
    exportV.columns.to_flat_index()
    exportV.columns = ['_'.join(x) for x in exportV.columns.to_flat_index()]
    exportV2 =exportV.rename(columns= {
        'r_e_p___c_o_u_n_t_r_i_e_s': 'rep_countries',
        'p_a_r___c_o_u_n_t_r_i_e_s': 'par_countries',
        'y_e_a_r': 'year',
        'e_l_e_m_e_n_t': 'element',
        'v_a_l_u_e': 'value',
        'i_t_e_m': 'item'})
    
    exportV3 = exportV2.sort_values('value',ascending=False).reset_index()
    #exportV3.head()
    exportV4 = exportV3.drop(columns=['element','index', 'year'])
    #exportV4.head(50)
    exportV5 = exportV4.to_json(orient='records')
    
    return exportV5

if __name__ == "__main__":
    app.debug = False
    app.run()

