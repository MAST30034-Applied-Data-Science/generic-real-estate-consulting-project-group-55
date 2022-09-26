import requests
import pandas as pd 
import numpy as np
import re
import time
import os
api = os.environ.get('api')
url = "https://api.domain.com.au/v1/listings/residential/_search?ids=1&api_key=key_fc2838ab4862c055e9db3d585b2a18d4"
# get k page data

def get_data(url):
    """
    function: download data
    param datas: the requested data
    """
    datas =[]
    for k in range(50):
        data = { "listingType":"Rent", "pageNumber": k,  "pageSize": 20, "locations":[{"state":"VIC"}]}
        resp = requests.post(url, data= str(data))
        #get json
        datas_part = resp.json()
        datas.extend(datas_part)
    return datas
datas = get_data(url)
#get dataframe columns


def get_columns(datas):
    """
    function: select the required columns
    param datas: required columns
    """
    if 'displayPrice' not in  datas['listing']['priceDetails']:
        price = 0
    if 'state'  not in  datas['listing']['propertyDetails']:
        state = 'null'
    for j in ['price', 'state', 'propertyType','bathrooms','bedrooms','carspaces','region','suburb', 'postcode','dateListed', 'listingSlug', 'latitude', 'longitude']:
        if j not in datas['listing']['propertyDetails']:
            datas['listing']['propertyDetails'][j] = 0    
    price = datas['listing']['priceDetails']['displayPrice']
    price =''.join(re.findall(r"\d+\.?\d*",price))
    state = datas['listing']['propertyDetails']['state']
    propertyType = datas['listing']['propertyDetails']['propertyType']
    bathrooms = datas['listing']['propertyDetails']['bathrooms']
    bedrooms = datas['listing']['propertyDetails']['bedrooms']
    carspaces = datas['listing']['propertyDetails']['carspaces']
    region = datas['listing']['propertyDetails']['region']
    suburb = datas['listing']['propertyDetails']['suburb']
    postcode = datas['listing']['propertyDetails']['postcode']
    dateListed = datas['listing']['dateListed']
    listingSlug = datas['listing']['listingSlug']
    latitude = datas['listing']['propertyDetails']['latitude']
    longitude = datas['listing']['propertyDetails']['longitude']
    return [price,state,propertyType,bathrooms,bedrooms, carspaces,region,suburb,postcode,dateListed, listingSlug, latitude, longitude]

def data_frame(datas):
    """
    function: put the required columns into a dataframe
    param datas: dataframe
    """
    # get dataframe
    rent_data = pd.DataFrame(columns = ['price', 'state', 'propertyType','bathrooms','bedrooms','carspaces','region','suburb', 'postcode','dateListed','listingSlug', 'latitude', 'longitude'])
    for i in range(len(datas)):
        rent_data.loc[len(rent_data.index)] = get_columns(datas[i])
    rent_data.reset_index(drop = False)
    return rent_data
time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))[:10]
path = 'rent_time' + time
data_frame(datas).to_csv("/home/ads/generic-real-estate-consulting-project-group-55/rent_data/" + path, index=False)