import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
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
        f"/api/v1.0/START_DATE<br/>"
        f"/api/v1.0/START_DATE/END_DATE"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of precipitation and date"""
    # Query the precipitation data
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()

    session.close()
    
    date = [result[0] for result in results]
    prcp = [result[1] for result in results]
    precip = pd.DataFrame(results, columns=['date', 'prcp'])
    precip = precip[precip['date'] > '2016-08-23']
    precip['prcp'] = precip['prcp'].fillna(0)
    precip = precip.groupby('date').sum()
    diction = precip.to_dict("date")

    return jsonify(diction["prcp"])


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station data"""
    # Query all stations
    station = pd.DataFrame(session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all(), columns=['id', 'station', 'name', 'latitude', 'longitude', 'elevation'])

    session.close()

    return station.to_json(orient = "split")


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the tobs data"""
    # Query all tobs data
    station = pd.DataFrame(session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).all(), columns=['id', 'station', 'date', 'prcp', 'tobs'])

    session.close()
    
    station_hist = station[station["date"] > '2016-08-23']
    station_hist = station_hist[station_hist["station"] == 'USC00519281']
    station_hist = station_hist[["date", "tobs"]]

    return station_hist.to_json(orient = "split")


@app.route("/api/v1.0/<start_date>")
def start(start_date):
    """Fetch the temperature summary for the selected time period"""
    if start_date <= '2016-08-23' or start_date > "2018-01-01":
        return jsonify({"error": f"Time period {start_date} not found."}), 404
    
    session = Session(engine)

    """Return the tobs data"""
    # Query all tobs data
    station = pd.DataFrame(session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).all(), columns=['id', 'station', 'date', 'prcp', 'tobs'])

    session.close()
    
    station_hist = station[station["date"] >= start_date]
    station_hist = station_hist[station_hist["station"] == 'USC00519281']
    low_temp = station_hist["tobs"].min()
    max_temp = station_hist["tobs"].max()
    avg_temp = station_hist["tobs"].mean()
    temp_dict = {"Low Temp": low_temp, "Max Temp": max_temp, "Average Temp": avg_temp}
    return jsonify(temp_dict)
   


@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    """Fetch the temperature summary for the selected time period"""
    if start_date <= '2016-08-23' or start_date > "2018-01-01":
        return jsonify({"error": f"Time period {start_date} not found."}), 404
    
    if end_date <= '2016-08-23' or end_date > "2018-01-01":
        return jsonify({"error": f"Time period {end_date} not found."}), 404
    
    if end_date < start_date:
        return jsonify({"error": f"Time period {end_date} comes before {start_date}."}), 404
    
    session = Session(engine)

    """Return the tobs data"""
    # Query all tobs data
    station = pd.DataFrame(session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).all(), columns=['id', 'station', 'date', 'prcp', 'tobs'])

    session.close()
    
    station_hist = station[station["date"] >= start_date]
    station_hist = station[station["date"] <= end_date]
    station_hist = station_hist[station_hist["station"] == 'USC00519281']
    low_temp = station_hist["tobs"].min()
    max_temp = station_hist["tobs"].max()
    avg_temp = station_hist["tobs"].mean()
    temp_dict = {"Low Temp": low_temp, "Max Temp": max_temp, "Average Temp": avg_temp}
    return jsonify(temp_dict)
    
    
if __name__ == '__main__':
    app.run(debug=True)
