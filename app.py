import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using 
    date as the key and prcp as the value.
    Return the JSON representation of your dictionary."""
    
    results = dict()
    for row in session.query(Measurement.date, Measurement.prcp).all():
        results[row[0]] = row[1]

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    
    results = session.query(Station.id, Station.name).all()
    
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most 
    active station for the last year of data."""
    
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    one_year

    temp_results = session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.date >= one_year).filter(Measurement.station == "USC00519281").all()
    
    session.close()


    return jsonify(temp_results)

@app.route("/api/v1.0/start/<start>")
def date_to_start(start):

        session = Session(engine)

        temp_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

        session.close()


        return jsonify(temp_start)

@app.route("/api/v1.0/startend/<start_date>/<end_date>")
def date_to_start_end(start_date, end_date):

        session = Session(engine)
        
        temp_duration = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

        session.close()


        return jsonify(temp_duration)

if __name__ == '__main__':
    app.run(debug=True)
