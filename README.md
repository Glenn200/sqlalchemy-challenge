# sqlalchemy-challenge
Overview
This data analysis repository of Hawaii climate data, stored in a sqlite database. Analysis is split up into the following sections:


Climate Analysis and Exploration
Climate Flask App

Climate Analysis and Exploration
Used Python and SQLAlchemy to do perform a climate analysis for Hawaii from climate database data provided. Analysis completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

Reflected Tables into SQLAlchemy ORM
The analysis was done inside a jupyter lab file. I used SQLAlchemy create_engine and SQLAlchemy automap_base() to connect to the sqlite database to reflect the tables into classes. Created classes as variables, called Station and Measurement.

Exploratory Climate Analysis
Analysis on the precipitation data from the last 12 months of available precipitation data. Created and stored data in a dataframe for plotting and visualizations.

Station Analysis
Outlines available climated measurement stations Calculate the lowest temperature recorded, the highest temperature recorded, and the average temperature of the most active station. Lastly, I plotted the results as a histogram.

Climate Flask App
Flask API developed based on the previous queries developed.

To run the app:

Copy, clone or download this repository to a local directory on your computer.
Change directory to the root directory (sqlalchemy-challenge) of this repository.
Run python app.py from the root directory (sqlalchemy-challenge). The app starts up at localhost:5000 by default.

Available routes/endpoints you can hit:

Route	Description
/	                This route is the home route. It lists all available routes.
/api/v1.0/precipitation	Retrieves the last 12 months of precipitation data, and returns the results. The format of the results is a JSON representation 				of a dictionary using the date as the key and the precipitation as the value.
/api/v1.0/stations	Weather monitoring stations in a JSON list.
/api/v1.0/tobs	        Dates and temperature observations from a year from the last available data point in a JSON list.
/api/v1.0/<start>	Minimum, average, and max temperatures for a given start date. The endpoint accepts dates using the YYYY-MM-DD date format 					(e.g., 2012-02-28).
/api/v1.0/<start>/<end>	Minimum, average, and max temperatures for a given start date-end date range. The endpoint accepts dates using the YYYY-MM-DD 					date format (e.g., 2012-02-28).