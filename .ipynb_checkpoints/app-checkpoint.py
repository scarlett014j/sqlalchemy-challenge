import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


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
        date_prcp = {}
        date_prcp["date"] = prcp
        date_prcp_l.append(date_prcp)
        
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
        station.append(station_dict)
        
    return jsonify(station)


@app.route("/api/v1.0/<start>")
def tobs():
    session= Session(engine)
    
    results = session.query(measurements.date, func.max(measurements.tobs), func.avg(measurements.tobs),func.min(measurements.tobs)).filter(measurements.date>='<start>').group_by.all()
    
    session(close)
    
    station_temp = []
    for station, tobs in results:
        stat_temp = {}
        stat_tem["Station"] = tobs
        station.append(station_dict)
        
    return jsonify(station_temp)



if __name__ == "__main__":
    app.run(debug = True)