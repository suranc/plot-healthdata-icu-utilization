#!/usr/bin/python3
import pandas as pd
import plotly.express as px

df = pd.read_csv('covid.csv')

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

# Generate icu_util.html interactive chart of the data, minus the above filters
fig.write_html('icu_util.html')
