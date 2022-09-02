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

# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def percipitation():
    print("Server received request for 'percipitation' page...")
    # Create our session (link) from Python to the DB

    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_perc = list(np.ravel(results))

    return jsonify(all_perc)

    

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    count_stat = func.count(Measurement.station).label('count')
    results = session.query(Measurement.station, count_stat).all()

    session.close()

    # Convert list of tuples into normal list
    all_stat = list(np.ravel(results))

    return jsonify(all_stat)


@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    """Return a list of all passenger names"""
    session = Session(engine)
    # Query all passengers
    
    results = session.query(Measurement.tobs).\
                        filter(Measurement.station == 'USC00519281').\
                        filter(Measurement.date >= a_year_ago).\
                        order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs) 

@app.route("/api/v1.0/<start>")
def start():
    print("Server received request for 'start' page...")
    session = Session(engine)
    # Query all passengers
    
    results = session.query(Measurement).filter(Measurement.date < a_year_ago).\
                        order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    temp_end = list(np.ravel(results))

    return jsonify(temp_end) 

@app.route("/api/v1.0/<start>/<end>")
def end():
    print("Server received request for 'end' page...")
    session = Session(engine)
    # Query all passengers
    
    results = session.query(Measurement).filter(Measurement.date >= a_year_ago).\
                        order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    temp_end = list(np.ravel(results))

    return jsonify(temp_end) 

if __name__ == "__main__":
    app.run(debug=True)

