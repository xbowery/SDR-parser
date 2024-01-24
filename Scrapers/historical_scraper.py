import requests as re
import zipfile
import pandas as pd
from datetime import datetime
import io

start_date = datetime.fromisoformat('2024-01-01')
end_date = datetime.today() - pd.Timedelta(days=1)

ASSET_CLASSES = ['COMMODITIES', 'CREDITS', 'FOREX', 'RATES']

# Download the zip file
for asset_class in ASSET_CLASSES:
    for date in pd.date_range(start_date, end_date):
        date = date.strftime('%Y_%m_%d')
        url = f'https://kgc0418-tdw-data-0.s3.amazonaws.com/cftc/eod/CFTC_CUMULATIVE_{asset_class}_{date}.zip'
        r = re.get(url)
        
        if r.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                z.extractall(f'..\\data\\{asset_class}')

