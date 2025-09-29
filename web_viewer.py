import os
import pandas as pd
import streamlit as st

from datetime import datetime, timedelta
from pymongo import MongoClient


mongourl = os.environ['mongourl']

client = MongoClient(mongourl)

st.title('DTCC Swap Data Repository Viewer')

st.write("This is a prototype of a viewer for the DTCC Swap Data Repository (taken from the latest data available in the repository).")

asset = st.multiselect('Choose Your Asset Class: ', ['Commodities', 'Credits', 'Forex', 'Rates'], ['Commodities'])

start_date = st.date_input('Select the starting date: ', datetime.today() - timedelta(days=2))
end_date = st.date_input('Select the ending date: ', datetime.today())

button = st.button('Submit')

asset_class = {'CO': 'Commodity', 'CR': 'Credit', 'FX': 'Forex', 'IR': 'Interest Rates'}

if button:
    df = pd.DataFrame()

    for item in asset:
        item_class = item.upper()
        db = client[item_class]

        temp_df = pd.DataFrame(
            db['all_records'].find(
                {'Event timestamp': {
                    '$gte': datetime.fromisoformat(start_date.strftime('%Y-%m-%d')), 
                    '$lte': datetime.fromisoformat(end_date.strftime('%Y-%m-%d'))
                    }
                }
            )
        )

        df = pd.concat([df, temp_df])

    df.rename(columns={'Product name': 'Trade Structure'}, inplace=True)
    df['Asset Class'] = df['Asset Class'].map(asset_class)
    if ':' in df['Trade Structure'].str:
        df['Trade Structure'] = df['Trade Structure'].str.split(':').str[1:]

    df = df[['_id', 'Asset Class', 'Trade Structure',
            'Effective Date', 'Event timestamp', 'Exchange rate', 'Exchange rate basis', 'Execution Timestamp',
            'Expiration Date', 'Fixed rate-Leg 1', 'Fixed rate-Leg 2', 'Notional amount-Leg 1',
            'Notional amount-Leg 2', 'Notional currency-Leg 1', 'Notional currency-Leg 2',
            'Option Premium Amount', 'Option Premium Currency', 'Option Style', 'Option Type',
            'Strike Price', 'Strike price currency/currency pair']]
    
    df = df.sort_values(by=['_id']).reset_index(drop=True)
    st.dataframe(df)