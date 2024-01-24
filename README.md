# SDR Parser and Viewer

This repository contains the codebase to deploy a minimalistic [Streamlit web application](dtcc-sdr-viewer.streamlit.app) to quickly view through all the daily reports from the [Depository Trust & Clearing Corporation repository](pddata.dtcc.com/gtr/).

There are 2 separate versions of the SDR Viewer in this repository: 

1. Proof-of-Concept for a deployed Streamlit web application (with only the past day's data available for space constraints) (found in the root directory)
2. Localhost viewing with a full set of data to view historical data (found in the `local_instance` directory)

## Steps to run the application locally

Do ensure you have Python 3.7+ and MongoDBCompass installed in your machine before running this application.

```bash
pip install requirements.txt

# To scrape the historical data locally
cd Scrapers

# Adjust the date you wish to start scraping from in line 7
python historical_scraper.py

cd ..

cd local_instance

# Save data to MongoDB instance
python database_saver.py

# View local application
python -m streamlit local_streamlit_viewer.py
```

You will be able to view the application running locally on your machine at this URL: `localhost:8501`.

## Web Application Overview

I created 2 GitHub Action workflows:

1. `scrape.yml`: This will automatically web scrape yesterday's DTCC cumulative reports and save the corresponding CSV file in this repository.
2. `update_db.yml`: This will automatically save the data to a Mongo Atlas cloud instance, and the data will be populated in the web application.


To see the deployed web application in action, view this [webpage](https://dtcc-sdr-viewer.streamlit.app/).