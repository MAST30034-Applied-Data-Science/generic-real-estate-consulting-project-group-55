import os
import time
import regex as re
import pandas as pd
from numpy import NaN
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pyecharts.charts import Pie, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# Ask user to input the region for the crawler and pages to crawl
region = str(input("Enter region to crawl: ").title())
if (region == ""):
    print("Please enter a valid region")
    exit()
pages = int(input("Enter pages to crawl: "))
if (pages < 1):
    print("Pages must be greater than 0")
    exit()


class AusRent():
    """
    This function is used to get the raw data from the website.
    """
    def __init__(self):
        self.url = 'https://www.domain.com.au/?mode=rent'
        service = ChromeService(
            executable_path=ChromeDriverManager().install())
        options = ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--log-level=3')
        self.wd = webdriver.Chrome(service=service, options=options)
        self.wd.implicitly_wait(10)
        self.region = region
        self.pages = pages
        # Open domain.com.au with rent tab
        
    """
    This function is used to open the url from the website.
    """
    def open(self):
        self.wd.get(self.url)

    """
    This function is used to search the region and get the raw data from the website.
    """
    def input(self):
        element = WebDriverWait(self.wd, 10).until(
            EC.presence_of_element_located((By.ID, "fe-pa-domain-home-typeahead-input")))
        element.send_keys(self.region)
        time.sleep(1)
        element.send_keys(Keys.UP)
        element.send_keys(Keys.ENTER)
        time.sleep(1)
        element.send_keys(Keys.ENTER)
        element = WebDriverWait(self.wd, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "css-99cvsw")))
        element.click()
        element = self.wd.find_element(
            By.ID, 'search-results-sort-by-filter-item-1')
        element.click()
        time.sleep(1)
        
    """
    This function is used to get the raw datas needed.
    """
    def get_raw_data(self):
        # Initialize the data frame and related lists
        df = pd.DataFrame()
        types = []
        postcodes = []
        prices = []
        bedrooms = []
        bathrooms = []
        garages = []
        links = []

        # Start crawling for multiple pages
        for i in range(int(self.pages)):
            print(f'Crawling page No.{i + 1}')

            # Wait for the page to load
            time.sleep(2)

            # Find type of properties
            type_el = self.wd.find_elements(By.CLASS_NAME, 'css-693528')
            for type in type_el:
                types.append(type.get_attribute('textContent'))
            # Find postcode of properties
            address_el = self.wd.find_elements(
                By.XPATH, '//span[@data-testid="address-line2"]')
            for address in address_el:
                try:
                    postcode = re.findall(
                        r'\d+', address.get_attribute('textContent'))[0]
                except:
                    postcode = NaN
                postcodes.append(postcode)
            # Find price of properties
            price_el = self.wd.find_elements(By.CLASS_NAME, 'css-mgq8yx')
            for price in price_el:
                price = price.text
                try:
                    price = int(re.match("\$(\d+(?:\,\d+)?)",
                                price).group(1).replace(',', ''))
                except:
                    price = NaN
                prices.append(price)
            # Find bedrooms & bathrooms & garages of properties
            features_el = self.wd.find_elements(By.CLASS_NAME, 'css-1t41ar7')
            for feature in features_el:
                bedroom = NaN
                bathroom = NaN
                try:
                    details = feature.find_elements(
                        By.CLASS_NAME, 'css-lvv8is')
                    bedroom = re.match(
                        "\d+", details[0].get_attribute('textContent'))[0]
                    bathroom = re.match(
                        "\d+", details[1].get_attribute('textContent'))[0]
                    garage = re.match(
                        "\d+", details[2].get_attribute('textContent'))[0]
                except:
                    if (bedroom == NaN or bathroom == NaN):
                        garage = NaN
                    else:
                        garage = 0
                bedrooms.append(bedroom)
                bathrooms.append(bathroom)
                garages.append(garage)
            # Find the link of properties
            link_el = self.wd.find_elements(
                By.CLASS_NAME, 'css-1y2bib4')
            for link in link_el:
                links.append(link.get_attribute('href'))

            # Go to next page if not the final loop
            if (i < self.pages):
                try:
                    self.wd.find_elements(
                        By.CLASS_NAME, 'css-1lkjjfg')[1].click()
                except:
                    try:
                        self.wd.find_elements(
                            By.CLASS_NAME, 'css-1lkjjfg')[0].click()
                    except:
                        print("No more page to crawl")
                        break

        print("-"*46, "Finished Page Crawling", "-"*46)
        df['Type'] = types
        df['Postcode'] = postcodes
        df['Price'] = prices
        df['Bedrooms'] = bedrooms
        df['Bathrooms'] = bathrooms
        df['Garages'] = garages
        df['Link'] = links
        # Save the raw data
        # df.to_csv(str(self.region).lower().replace(' ', '_').replace(',', '') + '_raw_data.csv')
        return df
    
    """
    This function is used to preprocess the raw data and save them to csv.
    """
    def clean_data(self):
        df = self.get_raw_data()
        # Drop the rows with NaN values
        df = df.dropna()
        df = df.reset_index(drop=True)

        # Get the last update date of each property (slow)
        dates = []
        for i in range(len(df['Link'])):
            self.wd.get(df['Link'][i])
            print(f'Crawling date of property No.{i + 1}')
            try:
                date = re.findall(r'\"updatedDate\":\"(.+?)\"', self.wd.find_element(
                    By.ID, "__NEXT_DATA__").get_attribute("innerHTML"))[0]
                # Keep only the date
                date = date.split('T')[0]
                dates.append(date)
            except:
                dates.append(NaN)
        df['Date'] = dates

        # Remove Link column
        df.drop(columns=['Link'], inplace=True)
        # Drop more rows with NaN values
        df = df.dropna()
        df = df.reset_index(drop=True)
        print("-"*38, "Finished Date Crawling & Data Cleaning", "-"*38)
        # Save the cleaned data
        df.to_csv(f"data{os.sep}raw{os.sep}" + str(self.region).lower().replace(
            ' ', '_').replace(',', '') + '_cleaned_data.csv')
        return df
    
    """
    This function is used to print the info in terminal.
    """
    def vis_data(self, df):
        print("-" * 50, 'Property Type Counts', '-' * 50)
        print(df.groupby('Type').size().to_string())
        print("-" * 49, 'Property Rent Averages', '-' * 49)
        print(df.groupby('Type')['Price'].mean().round(2).to_string())

    """
    This function is used to plot the data types.
    """
    def vis_pie(self, df, distinct):
        cate = df.groupby('Type').groups.keys()
        counts = df.groupby('Type').count()
        pie = (Pie(init_opts=opts.InitOpts(width='1280px', height='720px', page_title=f'{distinct} Property Types Counts'))
               .add('', [list(z) for z in zip(cate, counts['Price'])],
                    radius=['40%', '60%'],
                    label_opts=opts.LabelOpts(is_show=True),
                    )
               .set_global_opts(title_opts=opts.TitleOpts(title=f"{distinct} Property Types Counts"),
                                legend_opts=opts.LegendOpts(is_show=True))
               )

        pie.render(f"data{os.sep}raw{os.sep}{distinct} Property Type Counts.html")
        
    """
    This function is used to plot the data averages.
    """
    def vis_bar(self, df, distinct):
        x_vals = list(df.groupby('Type').groups.keys())
        xlen = len(x_vals)
        y_vals = df.groupby('Type')['Price'].mean().round(2)
        y_vals = y_vals.tolist()
        print(type(y_vals))
        bar = (Bar(init_opts=opts.InitOpts(width='1280px', height='720px', theme=ThemeType.ROMA, page_title=f'{distinct} Property Rent Averages'))
               .add_xaxis(x_vals)
               .add_yaxis('', y_vals)
               .set_series_opts(label_opts=opts.LabelOpts(is_show=True, font_size=15))
               .set_global_opts(title_opts=opts.TitleOpts(title=f'{distinct} Property Rent Averages'),
                                xaxis_opts=opts.AxisOpts(
                                    name='Property Types', axislabel_opts=opts.LabelOpts(rotate=0)),
                                yaxis_opts=opts.AxisOpts(name='Average Rent'))
               )
        bar.render(f'data{os.sep}raw{os.sep}{distinct} Property Rent Averages.html')
    
    """
    This function is the main function to run the program.
    """
    def query_project(self):
        self.open()
        self.input()
        df = self.clean_data()
        print(df)

        self.vis_data(df)
        self.vis_pie(df, region)
        self.vis_bar(df, region)
    
    """
    This function is used to sleep before closing the program.
    """
    def __del__(self):
        time.sleep(10)
        self.wd.close()

if __name__ == '__main__':
    query = AusRent()
    query.query_project()