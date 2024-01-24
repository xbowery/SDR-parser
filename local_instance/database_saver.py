from datetime import datetime
from pymongo import MongoClient

import numpy as np
import os
import pandas as pd
import traceback

client = MongoClient('localhost', 27017)
ASSET_CLASSES = ['COMMODITIES', 'CREDITS', 'FOREX', 'RATES']
id_trackers = {
    'COMMODITIES': [], 
    'CREDITS':[], 
    'FOREX':[], 
    'RATES':[]
}


def save_to_db_general(start_date, end_date):
    for asset in ASSET_CLASSES:
        db = client[asset]
        for date in pd.date_range(start_date, end_date):
            date = date.strftime('%Y_%m_%d')
            if os.path.isfile(f'..\\data\\CFTC_CUMULATIVE_{asset}_{date}.csv'):
                df = pd.read_csv(f'..\\data\\CFTC_CUMULATIVE_{asset}_{date}.csv', low_memory=False)
                df['_id'] = df['Dissemination Identifier']
                df['Effective Date'] = pd.to_datetime(df['Effective Date'])
                df['Event timestamp'] = pd.to_datetime(df['Event timestamp'])
                df['Execution Timestamp'] = pd.to_datetime(df['Execution Timestamp'])
                df['Expiration Date'] = pd.to_datetime(df['Expiration Date'])

                for record in df.to_dict('records'):
                    if str(record['Effective Date']) == 'NaT':
                        record['Effective Date'] = np.nan
                    if str(record['Event timestamp']) == 'NaT':
                        record['Event timestamp'] = np.nan
                    if str(record['Execution Timestamp']) == 'NaT':
                        record['Execution Timestamp'] = np.nan
                    if str(record['Expiration Date']) == 'NaT':
                        record['Expiration Date'] = np.nan

                    id_trackers[asset].append(record['_id'])

                db['all_records'].insert_many(df.to_dict('records'))
                os.remove(f'..\\data\\CFTC_CUMULATIVE_{asset}_{date}.csv')


def indexing_process():
    for asset in ASSET_CLASSES:
        db = client[asset]
        index_db = db['indexed']

        index_db.create_index({'Related IDs': 1})

        for id in id_trackers[asset]:
            record = db['all_records'].find_one({'_id': id})
            try:
                if str(record['Original Dissemination Identifier']) == 'nan':
                    doc = index_db.find_one({'_id': record['_id']})

                    if doc is None:
                        to_store = {
                            '_id': record['_id'],
                            'Related IDs': []
                        }

                        index_db.insert_one(to_store)
                else:
                    doc = index_db.find_one({'_id': record['Original Dissemination Identifier']})

                    if doc is None:
                        further_doc = index_db.find_one({'Related IDs': record['_id']})

                        if further_doc is None:
                            to_store = {
                                '_id': record['Original Dissemination Identifier'],
                                'Related IDs': [record['_id']]
                            }

                            index_db.insert_one(to_store)
                        else:
                            index_db.update_one({'_id': further_doc['_id']}, {'$push': {'Related IDs': record['_id']}})
                    else:
                        doc['Related IDs'].append(record['_id'])
                        index_db.update_one({'_id': record['Original Dissemination Identifier']}, {'$set': doc}, upsert=True)
            except:
                traceback.print_exc()


def clean_data():
    for asset in ASSET_CLASSES:
        db = client[asset]
        general_db = db['all_records']
        index_db = db['indexed']
        clean_db = db['cleaned']

        for record in index_db.find(no_cursor_timeout=True):
            if (len(record['Related IDs']) == 0):
                doc = general_db.find_one({'_id': record['_id']})
            else:
                doc_id = max(record['Related IDs'])
                doc = general_db.find_one({'_id': doc_id})
                doc['_id'] = record['_id']

            clean_db.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)


start_date = datetime.today() - pd.Timedelta(days=1)
end_date = datetime.today() - pd.Timedelta(days=1)
save_to_db_general(start_date, end_date)
indexing_process()
clean_data()