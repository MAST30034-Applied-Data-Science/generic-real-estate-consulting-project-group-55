import os
import pandas as pd
import urllib.request
from numpy import nan
from bs4 import BeautifulSoup

# Retrive the html of the website with given UA into the buffer
req = urllib.request.Request("https://www.australia-shoppings.com/malls-centres/victoria", headers={
                             'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
fp = urllib.request.urlopen(req)
webpage = fp.read()
content = webpage.decode("utf8")
fp.close()

# Referenced from https://www.geeksforgeeks.org/convert-html-table-into-csv-file-in-python/

# Initialize empty list
data = []

# Getting the header from the HTML file
soup = BeautifulSoup(content, 'html.parser')

# Main data retrieving
HTML_data = soup.find_all("ul")[3].find_all("li")

for element in HTML_data:
    sub_data = []
    for sub_element in element:
        try:
            sub_data.append(sub_element.get_text())
        except:
            continue
    data.append(sub_data)

# Storing the data into DataFrame
dataFrame = pd.DataFrame(data=data)

# Data cleaning
dataFrame.replace("", nan, inplace=True)
dataFrame.replace("\n", nan, inplace=True)
dataFrame.replace("\r", nan, inplace=True)
dataFrame.dropna(how='all', axis=1, inplace=True)
dataFrame.rename(columns={1: "Mall", 3: "Details"}, inplace=True)
dataFrame['Details'] = dataFrame['Details'].str.replace('phone:', '')
dataFrame['Details'] = dataFrame['Details'].str.replace('stores:', '')
dataFrame['Details'] = dataFrame['Details'].str.replace('GPS:', '')

# Split mall details into seperate columns
s = dataFrame["Details"].str.split('|')
dataFrame['Location'], _, dataFrame['Stores'] = s.str[0], s.str[1], s.str[2]
s = dataFrame["Location"].str.split(',')
dataFrame['State'], dataFrame['City'], dataFrame['Latitude'], dataFrame['Longitude'] = s.str[0], s.str[1], s.str[2], s.str[3]

# Remove leading and ending spaces of all columns
dataFrame = dataFrame.apply(lambda x: x.str.strip())

# Drop the original details column
dataFrame.drop(columns=["Details"], inplace=True)
dataFrame.drop(columns=['Location'], inplace=True)

# Converting DataFrame into CSV file
dataFrame.to_csv(f"data{os.sep}raw{os.sep}" + 'mall_info.csv')