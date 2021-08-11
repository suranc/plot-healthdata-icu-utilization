#!/usr/bin/python3
import pandas as pd
import plotly.express as px
import requests, json
import io

# Fetch JSON of dataset, and extract the latest CSV URL archive to download
url = requests.get("https://healthdata.gov/resource/qqte-vkut.json")
body = url.text
data = json.loads(body)
csv_url = data[len(data) - 1]['archive_link']['url']

# Download CSV and pass it to pandas to turn into a DataFrame
csv_url = requests.get(csv_url)
csv_string = csv_url.text
csv_buffer = io.StringIO(csv_string) # Turn csv_string into a file buffer to pass to read_csv
df = pd.read_csv(csv_buffer)

# Sort DataFrame by date
df.sort_values(by=['date'], inplace=True)

### Filter Data ###
# Drop rows with no utilization data
df.dropna(subset=['adult_icu_bed_utilization'])

# Remove Rows where the ICU utilization is above 1.5 (most likely garbage in)
i = df[(df.adult_icu_bed_utilization > 1.5)].index
df.drop(i, inplace=True)

# Drop rows prior to the mostly consistent data, starting 2020/07/14
df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d')
df_date = df.loc[(df['date'] > pd.to_datetime('2020/07/14'))]
####################

# Create line chart of data, grouped by state
fig = px.line(df_date, x = 'date', y = 'adult_icu_bed_utilization', color='state', line_group='state', title='Adult ICU Bed Utilization')

# Generate index.html interactive chart of the data, minus the above filters
fig.write_html('index.html')
