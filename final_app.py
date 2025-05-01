import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import altair as alt 

#load data
data = pd.read_csv("/Users/elisaschezzini/Desktop/data science project lifecycle/individual coursework/final cleaned traffic crashes in chicago.csv")

#preprocessing 
data['Crash_Date'] = pd.to_datetime(data['Crash_Date'], errors = 'coerce')
data['YEAR'] = data['Crash_Date'].dt.year
data['MONTH'] = data['Crash_Date'].dt.month_name()
data['DAY_OF_WEEK'] = data['Crash_Date'].dt.day_name()

#set page config
st.set_page_config(page_title="Chicago Traffic Fatalities Dashboard", layout="wide")

calendar_months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#sidebar filters
page = st.sidebar.selectbox('Navigate to:',['Overview', 'Charts', 'Data Tables', 'Key Insights'])
st.sidebar.header("Filter Data")
year_options = sorted(data['YEAR'].unique())
year = st.sidebar.multiselect("Select Year", options=year_options, default=year_options)
month = st.sidebar.multiselect("Select Month", options=calendar_months, default=calendar_months)

#filter data
filtered_data = data[(data['YEAR'].isin(year)) & (data['MONTH'].isin(month))]

#overview
if page == 'Overview':
    #title
    st.title("\U0001F6A8 Chicago Traffic Fatalities (Vision Zero)")
    
    #map of chicago
    st.subheader("Map of Chicago's Crash Locations")
    map_data = filtered_data[['Longitude', 'Latitude']]
    map_data = map_data.rename(columns={'Longitude':'lon', 'Latitude': 'lat'})
    st.map(map_data)
    st.markdown("---")

    st.subheader("Key Statistics")
    #keys (summary stats)
    key1, key2, key3 = st.columns(3)
    key1.metric(label="total fatalities", value=int(filtered_data.shape[0]))
    key2.metric(label="unique locations", value=filtered_data['Crash_Location'].nunique())
    key3.metric(label="years covered", value=f"{filtered_data['YEAR'].min()}-{filtered_data['YEAR'].max()}")
    st.markdown("---")
