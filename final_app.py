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
