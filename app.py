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
    results = { "names" : countries}
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


# for the year (to be changed)
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




@app.route("/yearslist")
def yearslist():
    # Create our session (link) from Python to the DB
    session = Session(db.engine)

    """Return a list of all years"""
    # Query all years
    list_year= session.query(worlddata.year).distinct().all()
   
    # print(list_year)
    session.close()

    # Convert list of tuples into normal list
    all_years = [x[0] for x in list_year]
    
    # all_years = list(np.ravel(list_year))
    results = { "years" : all_years}
    return jsonify(results)

@app.route("/importdata2011")
def importdata():
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
        worlddata.item).filter_by(year= 2011, element= 'Import Value').limit(1000).all()

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
    importV4 = importV3.drop(columns=['element','index', 'year'])
    #importV4.head(50)
    importV5 = importV4.to_json()
    
    return importV5

@app.route("/importdata2012")
def importdata():
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
        worlddata.item).filter_by(year= 2012, element= 'Import Value').limit(1000).all()

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
    importV4 = importV3.drop(columns=['element','index', 'year'])
    #importV4.head(50)
    importV5 = importV4.to_json()
    
    return importV5

@app.route("/importdata2013")
def importdata():
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
        worlddata.item).filter_by(year= 2013, element= 'Import Value').limit(1000).all()

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
    importV4 = importV3.drop(columns=['element','index', 'year'])
    #importV4.head(50)
    importV5 = importV4.to_json()
    
    return importV5

@app.route("/importdata2014")
def importdata():
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
        worlddata.item).filter_by(year= 2014, element= 'Import Value').limit(1000).all()

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
    importV4 = importV3.drop(columns=['element','index', 'year'])
    #importV4.head(50)
    importV5 = importV4.to_json()
    
    return importV5

@app.route("/importdata2015")
def importdata():
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
        worlddata.item).filter_by(year= 2015, element= 'Import Value').limit(1000).all()

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
    importV4 = importV3.drop(columns=['element','index', 'year'])
    #importV4.head(50)
    importV5 = importV4.to_json()
    
    return importV5

@app.route("/importdata2016")
def importdata():
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
        worlddata.item).filter_by(year= 2016, element= 'Import Value').limit(1000).all()

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
    importV4 = importV3.drop(columns=['element','index', 'year'])
    #importV4.head(50)
    importV5 = importV4.to_json()
    
    return importV5

@app.route("/importdata2017")
def importdata():
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
        worlddata.item).filter_by(year= 2017, element= 'Import Value').limit(1000).all()

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
    importV4 = importV3.drop(columns=['element','index', 'year'])
    #importV4.head(50)
    importV5 = importV4.to_json()
    
    return importV5

@app.route("/importdata2018")
def importdata():
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
        worlddata.item).filter_by(year= 2018, element= 'Import Value').limit(1000).all()

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
    importV4 = importV3.drop(columns=['element','index', 'year'])
    #importV4.head(50)
    importV5 = importV4.to_json()
    
    return importV5

@app.route("/importdata2019")
def importdata():
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
        worlddata.item).filter_by(year= 2019, element= 'Import Value').limit(1000).all()

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
    importV4 = importV3.drop(columns=['element','index', 'year'])
    #importV4.head(50)
    importV5 = importV4.to_json()
    
    return importV5

@app.route("/exportdata2011")
def exportdata():
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

@app.route("/exportdata2012")
def exportdata():
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

@app.route("/exportdata2013")
def exportdata():
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

@app.route("/exportdata2014")
def exportdata():
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
            element= 'Export Value', year = 2014).limit(1000).all()

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

@app.route("/exportdata2015")
def exportdata():
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
            element= 'Export Value', year = 2015).limit(1000).all()

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

