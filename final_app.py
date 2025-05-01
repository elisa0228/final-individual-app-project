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

