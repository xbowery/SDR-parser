import os
import pandas as pd
import streamlit as st

from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongourl = os.getenv('MONGOURL')

client = MongoClient(mongourl)

st.title('DTCC Swap Data Repository Viewer')

st.write("This is a prototype of a viewer for the DTCC Swap Data Repository (taken from the latest data available in the repository).")

asset = st.selectbox('Choose Your Asset Class: ', ['Commodities', 'Credits', 'Forex', 'Rates'])
asset = asset.upper()

start_date = st.date_input('Select the starting date: ', datetime(2024, 1, 1))
end_date = st.date_input('Select the ending date: ', datetime.today())

button = st.button('Submit')


if button:
    db = client[asset]

    df = db['all_records'].find(
        {'Event timestamp': {
            '$gte': datetime.fromisoformat(start_date.strftime('%Y-%m-%d')), 
            '$lte': datetime.fromisoformat(end_date.strftime('%Y-%m-%d'))
            }
        }
    )

    st.dataframe(df)