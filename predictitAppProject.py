# Import modules
import json
import requests
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#import pandas as pd
#pd.set_option('display.max_rows', None) #print all rows without truncating
#pd.options.mode.chained_assignment = None #hide SettingWithCopyWarning
#import numpy as np
#import datetime
import os
import zipfile #Economist
import urllib.request #Economist

class Data:
    def __init__(self):
        self.data = []
        #self.predictit_df = pd.DataFrame(self.data)
        self.resetData()

    def getData(self):
        return self.data

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
        self.data = []
        for p in jsondata['markets']:
            for k in p['contracts']:
                self.data.append([p['id'],p['name'],k['id'],k['name'],k['bestBuyYesCost'],k['bestBuyNoCost'],k['bestSellYesCost'],k['bestSellNoCost'],p['image']])
    
    def getMarketsWithID(self, marketID):
        marketWithSameID = []
        for listOfData in self.data:
            if(listOfData[0] == marketID):
                marketWithSameID.append(listOfData)
        return (marketWithSameID)