import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
         f"Available Routes:<br/>"
         f"/api/v1.0/precipitation"
         f" - Dates and temperature observations from the last year<br/>"

         f"/api/v1.0/stations"
         f" - List of stations<br/>"

         f"/api/v1.0/tobs"
         f" - Temperature Observations from the past year<br/>"

         f"/api/v1.0/<start>"
         f" - Minimum temperature, the average temperature, and the max temperature for a given start day, for example, /api/v1.0/2017-01-01<br/>"

         f"/api/v1.0/<start>/<end>"
         f" - Minimum temperature, the average temperature, and the max temperature for a given range of days (start-end),<br/> for example, /api/v1.0/2017-01-01/2017-01- 04"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Display a list of rain fall"""
    session = Session(engine)
    earliest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    results = session.query(Measurement.station, Measurement.date,Measurement.prcp).\
        filter(Measurement.date > dt.datetime.strptime(earliest_date[0],'%Y-%m-%d') - dt.timedelta(days = 365)).all()
    session.close()
    all_prcp = []
    for station, date, prcp in results:
        prcp_dict = {}
        prcp_dict['station'] = station
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        all_prcp.append(prcp_dict)   
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    """Return a list of stations"""
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    station_list=[]
    for result in results:
        sta_dict = {}
        sta_dict['station'] = result[0]
        sta_dict['name'] = result[1]
        sta_dict['latitude'] = result[2]
        sta_dict['longitude'] = result[3]
        sta_dict['elevation'] = result[4]
        station_list.append(sta_dict)
    return jsonify(station_list)      

@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most active station for the last year of data"""
    session = Session(engine)
    earliest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    active_station = (session.query(Measurement.station, func.count(Measurement.station)).\
                   group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all())
    most_active_station = active_station[0][0]
    results = session.query(Measurement.station, Measurement.date,Measurement.prcp).\
        filter(Measurement.date > dt.datetime.strptime(earliest_date[0],'%Y-%m-%d') - dt.timedelta(days = 365)).\
        filter(Measurement.station == most_active_station).all()
    session.close()
    most_act_prcp = []
    for result in results:
        most_act_dict = {}
        most_act_dict['station'] = result[0]
        most_act_dict['date'] = result[1]
        most_act_dict['prcp'] = int(result[2])
        most_act_prcp.append(most_act_dict)   
    return jsonify(most_act_prcp)

@app.route("/api/v1.0/<start>")
def start(start):
    # Docstring
    """Return a JSON list of tmin, tmax, tavg for the dates greater than or equal to the date provided"""
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                                func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()                             
    start_list = list(results)
    return jsonify(start_list)    

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Docstring
    """Return a JSON list of tmin, tmax, tavg for the dates in range of start date and end date inclusive"""
    session = Session(engine)
    results_dates = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                                  func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(
        Measurement.date <= end).all()
    between_dates_list = list(results_dates)
    session.close()
    return jsonify(between_dates_list)

if __name__ == '__main__':
    app.run(debug=True)