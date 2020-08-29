import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurements = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

app_index = {"Precipitation": "/api/v1.0/precipitation",
            "Station": "/api/v1.0/stations",
            "Most active Station info": "/api/v1.0/tobs",
            "Temperature Min, Max and Average (Specific Date)": "api/v1.0/<start>",
            "Temperature Min, Max and Average (Range of Dates)": "api/v1.0/<start>/<end>"}
@app.route("/")
def home():
    print("Below is a list of the available options:")
    return jsonify(app_index)

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    results = session.query(measurements.date, measurements.prcp).all()
    
    session.close()
    
    date_prcp = []
    for date, prcp in results:
        date_prcp_d = {}
        date_prcp_d[date] = prcp
        date_prcp.append(date_prcp_d)
        
    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = session.query(Station.id).all()
    
    session.close()
    
    station = []
    for id in results:
        station_d = {}
        station_d["Station"] = id
        station.append(station_d)
        
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    year = dt.datetime(2016, 7, 31)
    session = Session(engine)
    results = session.query(measurements.date, 
    func.max(measurements.tobs), func.avg(measurements.tobs),
    func.min(measurements.tobs)).filter(measurements.date>year).all()
    
    results_l = []

    session.close()
    for date, maxi, avg, mini in results:
        date_d={}
        date_d["date"] = date
        date_d["maximum"] = maxi
        date_d["avg"] = avg
        date_d["mini"] = mini
     
        results_l.append(date_d)

    return jsonify(results_l)

@app.route("/api/v1.0/<start>")
def starts(start):
    session = Session(engine)
    results = session.query(measurements.date, 
    func.max(measurements.tobs), func.avg(measurements.tobs), 
    func.min(measurements.tobs)).filter(measurements.date>=start).all()

    results_list = []
    session.close()

    for date, maxi, avg, mini in results:
        start_d={}
        start_d["date"] = date
        start_d["maxi"] = maxi
        start_d["avg"] = avg
        start_d["miń"] = mini
        results_list.append(start_d)

    return jsonify(results_list)

@app.route("/api/v1.0/<start>/<end>")
def dates(start, end):
    session = Session(engine)
    results = session.query(measurements.date, 
    func.max(measurements.tobs), func.avg(measurements.tobs), 
    func.min(measurements.tobs)).filter(measurements.date>=start).filter(measurements.date<=end).all()

    range_list = []
    session.close()

    for date1, maxi, avg, mini in results:
        start_d={}
        start_d["start"] = date1
        #start_d["end"] = date2
        start_d["maxi"] = maxi
        start_d["avg"] = avg
        start_d["miń"] = mini
        range_list.append(start_d)

    return jsonify(range_list)



if __name__ == "__main__":
    app.run(debug = True)