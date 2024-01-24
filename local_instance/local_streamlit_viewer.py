import pandas as pd
import streamlit as st

from datetime import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

st.title('DTCC Swap Data Repository Viewer')

st.write("This is a prototype of a viewer for the DTCC Swap Data Repository (taken from the local MongoDB instance).")

asset = st.selectbox('Choose Your Asset Class: ', ['Commodities', 'Credits', 'Forex', 'Rates'])
asset = asset.upper()

start_date = st.date_input('Select the starting date: ', datetime(2024, 1, 1))
end_date = st.date_input('Select the ending date: ', datetime.today())

button = st.button('Submit')


if button:
    db = client[asset]

    placeholder = st.empty()
    placeholder.write('Loading...')

    records = db['cleaned'].find(
        {'Event timestamp': {
            '$gte': datetime.fromisoformat(start_date.strftime('%Y-%m-%d')), 
            '$lte': datetime.fromisoformat(end_date.strftime('%Y-%m-%d'))
            }
        }
    )

    df = pd.DataFrame(records)
    df = df[['_id', 'Product name', 'Call amount-Leg 1', 'Call amount-Leg 2', 'Call currency-Leg 1', 'Call currency-Leg 2',
             'Effective Date', 'Event timestamp', 'Exchange rate', 'Exchange rate basis', 'Execution Timestamp', 
             'Expiration Date', 'Fixed rate-Leg 1', 'Fixed rate-Leg 2', 'Notional amount-Leg 1',
             'Notional amount-Leg 2', 'Notional currency-Leg 1', 'Notional currency-Leg 2', 
             'Option Premium Amount', 'Option Premium Currency', 'Option Style', 'Option Type',
             'Strike Price', 'Strike price currency/currency pair']]
    
    df.rename(columns={'Product name': 'Trade Structure'}, inplace=True)

    placeholder.empty()
    st.dataframe(df)