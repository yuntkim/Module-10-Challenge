# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL Toolkit 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import flask 
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine and connect to the SQLite database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Initialize Flask app, being sure to pass __name__
app = Flask(__name__)

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Routes
#################################################
@app.route("/") 
def home():
    return (
        f"Welcome to the Hawaii!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
)

@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    precipitation_dict = {date: precipitation for date, precipitation in precipitation}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations") 
def stations():
    station_count = session.query(Station).count()
    return jsonify(station_count)

@app.route("/api/v1.0/tobs") 
def tobs():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= year_ago).all()
    tobs_list = list(np.ravel(tobs))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>") 
def start_date(start):
    most_active = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    temp_list = list(np.ravel(most_active))
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>") 
def start_end_date(start,end):   
    most_active = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp_list = list(np.ravel(most_active))
    return jsonify(temp_list)

if __name__ == "__main__":
    app.run(debug=True)