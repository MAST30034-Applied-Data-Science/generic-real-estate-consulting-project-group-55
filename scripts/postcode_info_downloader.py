import os
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

# Retrive the html of the website with given UA into the buffer
req = urllib.request.Request("https://www.matthewproctor.com/full_australian_postcodes_vic", headers={
                             'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
fp = urllib.request.urlopen(req)
webpage = fp.read()
content = webpage.decode("utf8")
fp.close()

# Referenced from https://www.geeksforgeeks.org/convert-html-table-into-csv-file-in-python/

# Initialize empty list
data = []

# Getting the header from the HTML file
list_header = []
soup = BeautifulSoup(content, 'html.parser')
header = soup.find_all("table")[0].find("tr")

for items in header:
    try:
        list_header.append(items.get_text())
    except:
        continue

# Main data retrieving
HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

for element in HTML_data:
    sub_data = []
    for sub_element in element:
        try:
            sub_data.append(sub_element.get_text())
        except:
            continue
    data.append(sub_data)

# Storing the data into DataFrame
dataFrame = pd.DataFrame(data=data, columns=list_header)

# Converting DataFrame into CSV file
dataFrame.to_csv('/home/jnniu/Group55/generic-real-estate-consulting-project-group-55/data/raw/postcode_info.csv')
