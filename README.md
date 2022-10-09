# Generic Real Estate Consulting Project

Our goal is to explore the following three questions:

1. What are the most important internal and external features in predicting rental prices?
2. What are the top 10 suburbs with the highest predicted growth rate?
3. What are the most liveable and affordable suburbs according to your chosen metrics?

## Requirement

You should use 'pip install -r requirements.txt' at first.

## Internal Data we used

Domain Data (12/07/2022 - 01/10/2022)

## External Data we used

1. Park (The coordinates of the park are applied through Spatial DataShare)
2. School
3. Population
4. Yearly Income
5. Train Station
6. Past Rent

## Coding part - naming files (Both scirpts and notebooks)

- p1(part 1): Data Downloader & Data Pre-processing
- p2(part 2): Data Analysis
- p3(part 3): Three main quesitons
- p4(part 4): Summary
  
## Running Order

### Part 1

For scripts:

1. Run p1_mall_info_downloader.py.
2. Run p1_postcode_info_downloader.py.

Note: p1_api_download_data.py do not need to run. We have saved data in the folder "rent_data".

For notebooks:

1. Run p1_external_data_downloader.ipynb.
2. Run p1_external_data_preprocess.ipynb.

Note: p1_renew_api_data.ipynb combines the previous data and new data we got from domain and remove the duplicates. We have saved data after combining in the folder "rent_data" which named renew(15).csv.

### Part 2

1. Run p2_population_forecast and p2_affluence.ipynb.
2. Run the name of files starts from p2_distance _duration.ipynb.
3. Run p2_combine.ipynb.
4. Run p2_openrouteservice.ipynb.

### Part 3

1. Question 1: p3_internal_features.ipynb and p3_external_features.ipynb.
2. Question 2: p3_prediction.ipynb.
3. Question 3: p3_liveable.ipynb and p3_affordable.ipynb.

### Part 4

p4_summary.ipynb shows the summary of three main questions.
