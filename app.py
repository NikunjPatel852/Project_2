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
@app.route("/<country>/exporttotalvalue")
def exportcountryStats(country):
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

@app.route("/<country>/importtotalvalue")
def importcountryStats(country):
    print(country)
    import_rs = db.session.execute(""" 
    select sum(value) as value2, year
    from worlddata 
    where rep_countries = :country and element = 'Import Value'
    group by year
    """, {"country":country})
    import_stats = []
    for stat in import_rs:
        import_stats.append({
            "value": stat["value2"],
            "year": stat["year"]
        })
    return jsonify(import_stats)

@app.route("/<country>/importvaluedata")
def importvaldata(country):
    print(country)
    # Create our session (link) from Python to the DB
    # session = Session(db.engine)

    """Return a list of all country names"""
    # Query all Import Values 
    # import_data = session.query(
    #     worlddata.rep_countries, 
    #     worlddata.par_countries, 
    #     worlddata.year, 
    #     worlddata.element, 
    #     worlddata.value, 
    #     worlddata.item).filter_by(rep_countries= ':country',element= 'Import Value', {"country":country}).limit(10000).all()
    
    import_data = db.session.execute("""select rep_countries,par_countries,year,element,value,item from worlddata where element = 'Import Value' and rep_countries = :country""", {"country":country})
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

@app.route("/australia/importvaluedata")
def imvaluedata():
    #Create our session (link) from Python to the DB

    """Return a list of all country names"""
    #Query all Import Values 
    # element = ['Import Value', 'Import Quantity']
    # import_data = session.query(
    #     worlddata.rep_countries, 
    #     worlddata.par_countries, 
    #     worlddata.year, 
    #     worlddata.element,
    #     worlddata.unit, 
    #     worlddata.value, 
    #     worlddata.item).filter_by(rep_countries= 'Australia',element='Import Value').all()
    impor_data = db.session.execute("""select rep_countries,par_countries,year,element,unit,value,item from worlddata where rep_countries = 'Australia' and (element = 'Import Value' or element = 'Import Quantity')""")
    importV= pd.DataFrame(impor_data, columns=[
        'rep_countries', 
        'par_countries', 
        'year',
        'element',
        'unit', 
        'value', 
        'item'])
    
    importV.sort_values('value',ascending=False).groupby(['par_countries', 'item'])['value'].sum()
    importV.columns.get_level_values(0)
    importV.columns.to_flat_index()
    importV.columns = ['_'.join(x) for x in importV.columns.to_flat_index()]
    
    importV2 =importV.rename(columns= {
        'r_e_p___c_o_u_n_t_r_i_e_s': 'rep_countries',
        'p_a_r___c_o_u_n_t_r_i_e_s': 'par_countries',
        'y_e_a_r': 'year',
        'e_l_e_m_e_n_t': 'element',
        'u_n_i_t': 'unit',
        'v_a_l_u_e': 'value',
        'i_t_e_m': 'item'})
    
    importV3 = importV2.sort_values('value',ascending=False).reset_index()
    #importV3.head()
    importV4 = importV3.drop(columns=['index'])
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

@app.route("/australia/exportvaluedata")
def exportvaldata():
    # Create our session (link) from Python to the DB
    session = Session(db.engine)

    """Return a list of all country names"""
    # Query all passengers
    # exportv = session.query(
    #     worlddata.rep_countries, 
    #     worlddata.par_countries, 
    #     worlddata.year, 
    #     worlddata.element, 
    #     worlddata.value, 
    #     worlddata.item).filter_by(
    #         element= 'Export Value', year = 2012).limit(1000).all()
    exportv = db.session.execute("""select rep_countries,par_countries,year,element,unit,value,item from worlddata where rep_countries = 'Australia' and (element = 'Export Value' or element = 'Export Quantity')""")
    exportV= pd.DataFrame(exportv, columns=[
        'rep_countries', 
        'par_countries', 
        'year',
        'element',
        'unit', 
        'value', 
        'item'])
    
    exportV.sort_values('value',ascending=False).groupby(['par_countries', 'item'])['value'].sum()
    exportV.columns.get_level_values(0)
    exportV.columns.to_flat_index()
    exportV.columns = ['_'.join(x) for x in exportV.columns.to_flat_index()]
    exportV2 =exportV.rename(columns= {
        'r_e_p___c_o_u_n_t_r_i_e_s': 'rep_countries',
        'p_a_r___c_o_u_n_t_r_i_e_s': 'par_countries',
        'y_e_a_r': 'year',
        'e_l_e_m_e_n_t': 'element',
        'u_n_i_t': 'unit',
        'v_a_l_u_e': 'value',
        'i_t_e_m': 'item'})
    
    exportV3 = exportV2.sort_values('value',ascending=False).reset_index()
    #exportV3.head()
    exportV4 = exportV3.drop(columns=['index'])
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

