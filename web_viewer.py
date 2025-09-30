import os
import pandas as pd
import streamlit as st

from datetime import datetime, timedelta
from pymongo import MongoClient


mongourl = os.environ['mongourl']

client = MongoClient(mongourl)

st.title('DTCC Swap Data Repository Viewer')

st.write("This is a prototype of a viewer for the DTCC Swap Data Repository (taken from the latest data available in the repository).")

asset = st.multiselect('Choose Your Asset Class: ', ['Commodities', 'Credits', 'Forex', 'Rates'], ['Rates'])

start_date = st.date_input('Select the starting date: ', datetime.today() - timedelta(days=2))
end_date = st.date_input('Select the ending date: ', datetime.today())

button = st.button('Submit')

asset_class = {'CO': 'Commodity', 'CR': 'Credit', 'FX': 'Forex', 'IR': 'Rates'}

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
    try:
        df['Trade Structure'] = df['Trade Structure'].str.split(':').str[1:]
    except:
        pass
    
    if df['Asset Class'].unique()[0] != 'Rates':
        df = df[['_id', 'Asset Class', 'Trade Structure',
                'Effective Date', 'Event timestamp', 'Exchange rate', 'Exchange rate basis', 'Execution Timestamp',
                'Expiration Date', 'Fixed rate-Leg 1', 'Fixed rate-Leg 2', 'Notional amount-Leg 1',
                'Notional amount-Leg 2', 'Notional currency-Leg 1', 'Notional currency-Leg 2',
                'Option Premium Amount', 'Option Premium Currency', 'Option Style', 'Option Type',
                'Strike Price', 'Strike price currency/currency pair']]
    else:
        df = df[['_id', 'Asset Class', 'UPI Underlier Name', 'Effective Date', 'Event timestamp', 'Exchange rate', 'Exchange rate basis', 'Execution Timestamp',
                'Expiration Date', 'First exercise date', 'Fixed rate-Leg 1', 'Fixed rate-Leg 2', 'Notional amount-Leg 1',
                'Notional amount-Leg 2', 'Notional currency-Leg 1', 'Notional currency-Leg 2',
                'Notional amount in effect on associated effective date-Leg 1', 'Notional amount in effect on associated effective date-Leg 2',
                'Effective date of the notional amount-Leg 1', 'Effective date of the notional amount-Leg 2',
                'End date of the notional amount-Leg 1', 'End date of the notional amount-Leg 2',
                'Option Premium Amount', 'Option Premium Currency', 'Spread-Leg 1', 'Spread-Leg 2',
                'Strike Price', 'Strike price currency/currency pair']]
    
    df = df.sort_values(by=['_id']).reset_index(drop=True)
    st.dataframe(df)
