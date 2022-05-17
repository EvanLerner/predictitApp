# Import modules
import json
import requests
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
pd.set_option('display.max_rows', None) #print all rows without truncating
pd.options.mode.chained_assignment = None #hide SettingWithCopyWarning
import numpy as np
import datetime
import os
import zipfile #Economist
import urllib.request #Economist

class Data:
    def __init__(self):
        data = []
        self.predictit_df = pd.DataFrame(data)
        self.resetData()

    def getdf(self):
        return self.predictit_df

    # Replace null values with zero
    def dict_clean(self, items):
        result = {}
        for key, value in items:
            if value is None:
                value = 0
            result[key] = value
        return result

    def resetData(self):
        # Pull in market data from PredictIt's API
        Predictit_URL = "https://www.predictit.org/api/marketdata/all/"
        Predictit_response = requests.get(Predictit_URL)
        jsondata = Predictit_response.json()

        dict_str = json.dumps(jsondata)
        jsondata = json.loads(dict_str, object_pairs_hook=self.dict_clean)
        # Market data by contract/price in dataframe
        data = [];
        for p in jsondata['markets']:
            for k in p['contracts']:
                data.append([p['id'],p['name'],k['id'],k['name'],k['bestBuyYesCost'],k['bestBuyNoCost'],k['bestSellYesCost'],k['bestSellNoCost']])

        # Pandas dataframe named 'predictit_df'

        self.predictit_df = pd.DataFrame(data)

        # Update dataframe column names
        self.predictit_df.columns=['Market_ID','Market_Name','Contract_ID','Contract_Name','PredictIt_Yes','bestBuyNoCost','BestSellYesCost','BestSellNoCost']

d1 = Data()
print(d1.getdf().head(1).values.tolist())


