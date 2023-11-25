# Import the necessary dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes

# Root route with information about available API routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

# API route for precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Retrieve the most recent date in the database
    session = Session(engine)
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    
    # Calculate the date one year ago from the most recent date
    one_year_ago = (pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)).strftime("%Y-%m-%d")
    
    # Query precipitation data for the last year
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    session.close()
    
    # Convert the query results to a dictionary
    precipitation_data_list = []
    for date, prcp in precipitation_data:
        precipitation_data_dict = {}
        precipitation_data_dict[date] = prcp
        precipitation_data_list.append(precipitation_data_dict)
    
    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data_list)

# API route for station data
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    
    # Convert the query results to a list of dictionaries
    stations_list = []
    for id, s, n, lat, lon, el in stations:
        stations_dict = {}
        stations_dict['id'] = id
        stations_dict['station'] = s
        stations_dict['name'] = n
        stations_dict['latitude'] = lat
        stations_dict['longitude'] = lon
        stations_dict['elevation'] = el
        stations_list.append(stations_dict)
    
    # Return the JSON representation of the list
    return jsonify(stations_list)

# API route for temperature observations (tobs) data
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    # Query the most active station based on the number of observations
    stations_activity = (
        session.query(Measurement.station, func.count())
        .group_by(Measurement.station)
        .order_by(func.count().desc())
        .all()
    )
    
    # Retrieve the most recent date in the database
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    
    # Calculate the date one year ago from the most recent date
    one_year_ago = (pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)).strftime("%Y-%m-%d")
    
    # Query temperature observations for the last year from the most active station
    most_active_temps = session.query(Measurement.date, Measurement.tobs).filter(
        and_(Measurement.station == stations_activity[0][0], Measurement.date >= one_year_ago)
    ).all()
    
    session.close()
    
    # Convert the query results to a list of dictionaries
    temps_list = []
    for date, tmp in most_active_temps:
        temps_dict = {}
        temps_dict[date] = tmp
        temps_list.append(temps_dict)
    
    # Return the JSON representation of the list
    return jsonify(temps_list)

# API route for temperature statistics based on a start date
@app.route("/api/v1.0/<start>")
def stemps(start):
    session = Session(engine)
    
    # Query temperature statistics (min, max, avg) for a given start date
    temp_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(
        Measurement.date >= start
    ).all()
    
    session.close()
    
    # Convert the query results to a list of dictionaries
    temp_stats_list = []
    for min, max, avg in temp_stats:
        temp_stats_dict = {}
        temp_stats_dict['min_temp'] = min
        temp_stats_dict['max_temp'] = max
        temp_stats_dict['avg_temp'] = avg
        temp_stats_list.append(temp_stats_dict)
    
    # Return the JSON representation of the list
    return jsonify(temp_stats_list)

# API route for temperature statistics based on a start and end date
@app.route("/api/v1.0/<start>/<end>")
def setemps(start, end):
    session = Session(engine)
    
    # Query temperature statistics (min, max, avg) for a given start and end date
    temp_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(
        and_(Measurement.date >= start, Measurement.date <= end)
    ).all()
    
    session.close()
    
    # Convert the query results to a list of dictionaries
    temp_stats_list = []
    for min, max, avg in temp_stats:
        temp_stats_dict = {}
        temp_stats_dict['min_temp'] = min
        temp_stats_dict['max_temp'] = max
        temp_stats_dict['avg_temp'] = avg
        temp_stats_list.append(temp_stats_dict)
    
    # Return the JSON representation of the list
    return jsonify(temp_stats_list)

# Run the Flask app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
