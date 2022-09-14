import pandas as pd 
# please note old is the data from the last code run, new is data from this code run
old = pd.read_csv("/home/ads/generic-real-estate-consulting-project-group-55/rent_data/renew(11)", index_col=0)
new = pd.read_csv("/home/ads/generic-real-estate-consulting-project-group-55/rent_data/rent_time2022-09-11", index_col=0)
def renew_data(old, new):
    renew = pd.concat([old, new])
    renew = renew.reset_index(drop = True).drop_duplicates(subset = ['listingSlug'])
    return renew
renew_data(old, new).to_csv("/home/ads/generic-real-estate-consulting-project-group-55/rent_data/renew(12)")
