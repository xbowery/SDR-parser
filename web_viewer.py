import pandas as pd
import streamlit as st

from datetime import datetime, timedelta

st.title('DTCC Swap Data Repository Viewer')

st.write("This is a prototype of a viewer for the DTCC Swap Data Repository (taken from the latest data available in the repository).")

asset = st.selectbox('Choose Your Asset Class: ', ['Commodities', 'Credits', 'Forex', 'Rates'])
asset = asset.upper()

start_date = st.date_input('Select the starting date: ', datetime(2024, 1, 1))
end_date = st.date_input('Select the ending date: ', datetime.today())

button = st.button('Submit')


if button:
    file_date = (datetime.today() - timedelta(days=2)).strftime('%Y_%m_%d')
    file_name = f"CFTC_CUMULATIVE_{asset}_{file_date}.csv"

    df = pd.read_csv(f'data\\{file_name}', low_memory=False)
    df['Event timestamp'] = pd.to_datetime(df['Event timestamp'])
    df['Execution Timestamp'] = pd.to_datetime(df['Execution Timestamp'])
    df['Expiration Date'] = pd.to_datetime(df['Expiration Date'])
    df['Effective Date'] = pd.to_datetime(df['Effective Date'])

    df = df[['Dissemination Identifier', 'Product name', 'Call amount-Leg 1', 'Call amount-Leg 2', 'Call currency-Leg 1', 'Call currency-Leg 2',
            'Effective Date', 'Event timestamp', 'Exchange rate', 'Exchange rate basis', 'Execution Timestamp', 
            'Expiration Date', 'Fixed rate-Leg 1', 'Fixed rate-Leg 2', 'Notional amount-Leg 1',
            'Notional amount-Leg 2', 'Notional currency-Leg 1', 'Notional currency-Leg 2', 
            'Option Premium Amount', 'Option Premium Currency', 'Option Style', 'Option Type',
            'Strike Price', 'Strike price currency/currency pair']]

    df.rename(columns={
        'Dissemination Identifier': '_id',
        'Product name': 'Trade Structure'
        }, inplace=True)

    st.dataframe(df)