from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient

import numpy as np
import os
import pandas as pd

load_dotenv("./.env.prod")

mongourl = os.getenv('MONGOURL')
client = MongoClient(mongourl)


ASSET_CLASSES = ['COMMODITIES', 'CREDITS', 'FOREX', 'RATES']

for asset in ASSET_CLASSES:
    client.drop_database(asset)

    file_date = (datetime.today() - timedelta(days=1)).strftime('%Y_%m_%d')
    file_name = f"data\\CFTC_CUMULATIVE_{asset}_{file_date}.csv"

    df = pd.read_csv(file_name, low_memory=False)
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
    
    df_dict = df.to_dict('records')

    db = client[asset]

    for item in df_dict:
        if str(item['Effective Date']) == 'NaT':
            item['Effective Date'] = np.nan
        if str(item['Event timestamp']) == 'NaT':
            item['Event timestamp'] = np.nan
        if str(item['Execution Timestamp']) == 'NaT':
            item['Execution Timestamp'] = np.nan
        if str(item['Expiration Date']) == 'NaT':
            item['Expiration Date'] = np.nan

    db['all_records'].insert_many(df_dict)

    db['all_records'].create_index({'Event timestamp': 1})

    os.remove(file_name)
