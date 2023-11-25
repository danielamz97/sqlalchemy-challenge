# SQL Alchemy Challenge

## Overview

This project is a data analysis and visualization tool that utilizes Jupyter Notebook, SQLite database, and Flask API. It provides insights into weather data, station information, and offers a user-friendly API for accessing specific datasets.

## Features

### Jupyter Notebook Database Connection

- Utilizes SQLAlchemy to connect to an SQLite database.
- Reflects tables into classes using SQLAlchemy automap_base().
- Saves references to the classes for station and measurement.
- Establishes a connection between Python and the database using a SQLAlchemy session.
- Ensures proper closure of the session at the end of the notebook.

### Precipitation Analysis

- Identifies the most recent date in the dataset.
- Retrieves and analyzes precipitation data for the last year.
- Stores query results in a Pandas DataFrame for easy manipulation.
- Generates a sorted plot of precipitation data over time.
- Provides summary statistics for the precipitation data.

### Station Analysis

- Determines the number of stations in the dataset.
- Lists stations and their observation counts in descending order, identifying the most active station.
- Calculates the min, max, and average temperatures for the most active station.
- Retrieves the previous 12 months of temperature observation (TOBS) data for the most active station.
- Stores TOBS data in a Pandas DataFrame and creates a histogram for visualization.

### API Implementation

- Establishes a Flask application with SQLite connection.
- Displays available routes on the landing page for user reference.

#### Static Routes

- Precipitation Route: Returns JSON with date as the key and precipitation as the value for the last year.
- Stations Route: Returns JSONified data for all stations in the database.
- TOBS Route: Returns JSONified data for the most active station for the last year.

#### Dynamic Routes

- Start Route: Accepts a start date parameter and returns min, max, and average temperatures from the start date to the end of the dataset.
- Start/End Route: Accepts start and end date parameters, returning min, max, and average temperatures for the specified date range.


## Credits

Developed by [Daniela Montiel Zuñiga].

Happy exploring!
