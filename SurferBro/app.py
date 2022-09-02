# 1. import Flask
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Keys = Base.classes.keys

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

a_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#percipitation link
@app.route("/api/v1.0/precipitation")
def percipitation():
    print("Server received request for 'percipitation' page...")
    # Create our session (link) from Python to the DB

    session = Session(engine)

    """Return a list of all passenger names"""
    
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    
    all_perc = list(np.ravel(results))

    return jsonify(all_perc)

    
#stations link
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    session = Session(engine)

    """Return a list of all passenger names"""
    
    count_stat = func.count(Measurement.station).label('count')
    results = session.query(Measurement.station, count_stat).all()

    session.close()

    
    all_stat = list(np.ravel(results))

    return jsonify(all_stat)

#tobs link
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    """Return a list of all passenger names"""
    session = Session(engine)
   
    
    results = session.query(Measurement.tobs).\
                        filter(Measurement.station == 'USC00519281').\
                        filter(Measurement.date >= a_year_ago).\
                        order_by(Measurement.date).all()

    session.close()

    
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs) 
#start link
@app.route("/api/v1.0/<start>")
def start(start):
    #print(start)
    print("Server received request for 'start' page...")
    session = Session(engine)
    
    #print(start)
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date > start).\
                        order_by(Measurement.date).all()

    session.close()

    
    temp_end = list(np.ravel(results))

    return jsonify(temp_end) 
#start and end link
@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    print("Server received request for 'end' page...")
    session = Session(engine)
    
    
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= start).\
                        filter(Measurement.date <= end).\
                        order_by(Measurement.date).all()

    session.close()

    
    temp_end = list(np.ravel(results))

    return jsonify(temp_end) 

if __name__ == "__main__":
    app.run(debug=True)

