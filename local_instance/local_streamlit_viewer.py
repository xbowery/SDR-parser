import pandas as pd
import streamlit as st

from datetime import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

st.title('DTCC Swap Data Repository Viewer')

st.write("This is a prototype of a viewer for the DTCC Swap Data Repository (taken from the local MongoDB instance).")

asset = st.multiselect('Choose Your Asset Class: ', ['Commodities', 'Credits', 'Forex', 'Rates'], ['Commodities'])

start_date = st.date_input('Select the starting date: ', datetime(2024, 1, 1))
end_date = st.date_input('Select the ending date: ', datetime.today())

button = st.button('Submit')


if button:
    df = pd.DataFrame()
    placeholder = st.empty()
    placeholder.write('Loading...')

    for item in asset:
        item_class = item.upper()
        db = client[item_class]

        records = db['cleaned'].find(
            {'Event timestamp': {
                '$gte': datetime.fromisoformat(start_date.strftime('%Y-%m-%d')), 
                '$lte': datetime.fromisoformat(end_date.strftime('%Y-%m-%d'))
                }
            }
        )

        temp_df = pd.DataFrame(records)
        
        temp_df.rename(columns={'Product name': 'Trade Structure'}, inplace=True)
        temp_df['Asset Class'] = temp_df['Trade Structure'].str.split(':').str[0]
        temp_df['Trade Structure'] = temp_df['Trade Structure'].str.split(':').str[1:]

        temp_df = temp_df[['_id', 'Asset Class', 'Trade Structure', 'Call amount-Leg 1', 'Call amount-Leg 2', 'Call currency-Leg 1', 'Call currency-Leg 2',
                'Effective Date', 'Event timestamp', 'Exchange rate', 'Exchange rate basis', 'Execution Timestamp', 
                'Expiration Date', 'Fixed rate-Leg 1', 'Fixed rate-Leg 2', 'Notional amount-Leg 1',
                'Notional amount-Leg 2', 'Notional currency-Leg 1', 'Notional currency-Leg 2', 
                'Option Premium Amount', 'Option Premium Currency', 'Option Style', 'Option Type',
                'Strike Price', 'Strike price currency/currency pair']]
        
        df = pd.concat([df, temp_df])

    df = df.sort_values(by=['_id']).reset_index(drop=True)

    placeholder.empty()
    st.dataframe(df)