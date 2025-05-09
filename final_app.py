import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import altair as alt 

#load data from raw github url
data = pd.read_csv("https://raw.githubusercontent.com/elisa0228/final-individual-app-project/refs/heads/main/final%20cleaned%20traffic%20crashes%20in%20chicago.csv")
#preprocessing 
data['Crash_Date'] = pd.to_datetime(data['Crash_Date'], errors = 'coerce') #convert crash date to datetime
data['YEAR'] = data['Crash_Date'].dt.year #extract year
data['MONTH'] = data['Crash_Date'].dt.month_name() #extract month name
data['DAY_OF_WEEK'] = data['Crash_Date'].dt.day_name() #extract day of week
data['HOUR'] = data['Crash_Date'].dt.hour #extract hour of crash

#set page config
st.set_page_config(page_title="Chicago Traffic Fatalities Dashboard", layout="wide")

#define ordered list of month for charts and tables
calendar_months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#sidebar filters
page = st.sidebar.selectbox('Navigate to:',['Outline', 'Charts', 'Data Tables', 'Key Recap']) #navigation between app sections
st.sidebar.header("Filter Data")
year_options = sorted(data['YEAR'].unique()) #list available years from data
year = st.sidebar.multiselect("Select Year", options=year_options, default=year_options) #multi-select year
month = st.sidebar.multiselect("Select Month", options=calendar_months, default=calendar_months) #multi-select month 

#filter data
filtered_data = data[(data['YEAR'].isin(year)) & (data['MONTH'].isin(month))]

#outline page
if page == 'Outline':
    #title
    st.title("\U0001F6A8 Chicago Traffic Fatalities (Vision Zero)")
    
    #map of chicago
    st.subheader("Map of Chicago's Crash Locations")
    map_data = filtered_data[['Longitude', 'Latitude']] #extract coordinates
    map_data = map_data.rename(columns={'Longitude':'lon', 'Latitude': 'lat'}) #rename for st.map()
    st.map(map_data) #display map
    st.markdown("---")

    st.subheader("Key Statistics")
    #keys (summary stats)
    key1, key2, key3 = st.columns(3) #three summary stats
    key1.metric(label="total fatalities", value=int(filtered_data.shape[0])) #total rows
    key2.metric(label="unique locations", value=filtered_data['Crash_Location'].nunique()) #unique crash locations
    key3.metric(label="years covered", value=f"{filtered_data['YEAR'].min()}-{filtered_data['YEAR'].max()}") #range of years
    st.markdown("---")

#charts page
elif page == 'Charts':
    st.title("Visualisations")

    #visualisations
    #bar chart of fatalities over time 
    st.subheader("Monthly Fatalities")
    st.caption("you can select full screen to see the graph clearer")
    month_counts = (filtered_data['MONTH'].value_counts().reindex(calendar_months, fill_value=0)) #count fatalities
    bar_chart, ax = plt.subplots(figsize=(10,5))
    ax.bar(month_counts.index, month_counts.values, color='palevioletred') #plot bar chart
    ax.set_title("Number of Fatalities per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Fatalities")
    plt.xticks(rotation=45) #rotate x-axis labels
    st.pyplot(bar_chart) #display chart
    st.markdown("---")

    #pie chart of crash victim breakdown
    st.subheader("Crash Victim Breakdown")
    if 'Victim' in filtered_data.columns:
        fig_type = px.pie(filtered_data, names='Victim', title='Type of Victims') #pie chart
        st.plotly_chart(fig_type, use_container_width=True)
    st.markdown("---")

    #line chart of fatalities over time
    st.subheader("Monthly Fatalities by Year")
    st.caption("interactive chart showing month, value and year")
    monthly_by_year = (filtered_data.groupby(['YEAR','MONTH']).size().reset_index(name='Fatalities')) #group data
    monthly_by_year['MONTH']=pd.Categorical(monthly_by_year['MONTH'], categories=calendar_months, ordered=True) #ensure month categorical order
    monthly_by_year = monthly_by_year.sort_values(['MONTH', 'YEAR']) #sort values
    pivot_df = monthly_by_year.pivot(index='MONTH', columns='YEAR',values='Fatalities') #pivot table for streamlit line chart
    pivot_df = pivot_df.loc[calendar_months] #ensure row order
    st.line_chart(pivot_df) #display line chart
    st.markdown("---")

    #area chart grouped by victim type
    st.subheader("Monthly Fatalities by Victim Type")
    st.caption("interactive chart showing months, value and victim type")
    monthly_victims = (filtered_data.groupby(['MONTH', 'Victim']).size().reset_index(name='Fatalities')) #group data
    monthly_victims['MONTH']=pd.Categorical(monthly_victims['MONTH'], categories=calendar_months, ordered=True)
    area_df = monthly_victims.pivot(index='MONTH', columns='Victim', values='Fatalities') #pivot for streamlit
    area_df = area_df.loc[calendar_months]
    st.area_chart(area_df) #display area chart
    st.markdown("---")

    #altair chart
    #year determined colour and N mean years is a nominal (categorical) variable
    st.subheader("Crash Locations by Year")
    st.caption("interactive chart showing latitude, longitude and year")
    alt_data = filtered_data[['Latitude', 'Longitude', 'YEAR']] #extract fields
    alt_chart = alt.Chart(alt_data).mark_circle(size=60).encode(x='Longitude', y='Latitude', color='YEAR:N', tooltip=['Latitude', 'Longitude', 'YEAR']).properties(width=700, height=400).interactive()
    st.altair_chart(alt_chart, use_container_width=True)
    st.markdown("---")

#data tables page
elif page == 'Data Tables':
    #title
    st.title("Data Tables")

    st.subheader("Top Victims in Order of Highest Fatality Rates")
    top_victims = filtered_data['Victim'].value_counts().reset_index()
    top_victims.columns = ['Victim Type', 'Fatalities']
    top_victims.index = top_victims.index + 1 #start index at 1
    st.dataframe(top_victims) #display victim table
    st.markdown("---")

    st.subheader("Top 5 Most Common Crash Locations via Street")
    top_locations = filtered_data['Crash_Location'].value_counts().head(5).reset_index()
    top_locations.columns = ['Location', 'Count']
    top_locations.index = top_locations.index + 1
    st.dataframe(top_locations) #display location table
    st.markdown("---")

    st.subheader("The Count of Fatalities per Month")
    common_months = filtered_data['MONTH'].value_counts().reindex(calendar_months).reset_index()
    common_months.columns = ['Month', 'Fatalities']
    st.dataframe(common_months, hide_index=True)
    st.markdown("---")

    st.subheader("The Count of Fatalities per Year")
    common_years = filtered_data['YEAR'].value_counts().sort_index().reset_index()
    common_years.columns = ['Year', 'Fatalities']
    st.dataframe(common_years, hide_index=True)
    st.markdown("---")

    st.subheader("The Count of Times for Fatalities")
    st.caption("times on dataset are 12 hour this table is 24 hour")
    common_hours = filtered_data['HOUR'].value_counts().sort_index().reset_index()
    common_hours.columns = ['Hour', 'Fatalities']
    common_hours['Hour'] = common_hours['Hour'].apply(lambda h: f"{h:02d}:00") #format hour from 0 to 00:00
    st.dataframe(common_hours, hide_index=True) #display hours table

#key recap page
elif page == 'Key Recap':
    st.title("Key Recap from Chicago Traffic Fatality Data")
    st.markdown("""
### Summary
 This analysis explores traffic crash fatalities in Chicago, supporting the city's Vision Zero initiative to eliminate traffic deaths by 2026. The insights presented are grounded in patterns observed through charts, maps, and statistics based on the cleaned dataset.
                
### Victim Profiles
- **PEDESTRIANS** represent the largest proportion of fatalities, followed by **DRIVERS** and **PASSENGERS**.
- **SCOOTERS** account for the fewest fatalities but remain a vulnerabl group, ofen impacted in dense urban zones.
               
### Temporal Patterns
- **JULY and SEPTEMBER** consistently record the **highest number of fatalities**, suggesting seasonal influenced such as increased traffic, events, and longer daylight hours.
- Fatalities are also high in **OCTOBER**, possibly linked to changing light conditions and weather.
- The most dangerous **time of day** are typically **late evening to early morning hours (7pm to 2am)**
                
### Spatial Distribution
- Crashed cluster in  major arterial roads and intersections.
- **Top 5 crash hotspots** include well-known high risk corridors in the city where visibility, volumne, or speed contribute to fatal outcomes.
                
### Yearly Trends
- While fluctuations occur year to year, recent years such as **2020 and 2021** show significant numbers despite lower traffic volume due to the pandemic - possibly due to increased speeding on emptier roads.
- Fatalities are also high in **2022**, most likely linked to the recovery of the pandemic as more people or going on holidays and outings and shopping.
- Long-term trends show the importance of consistent enforcement and infrastructure improvements.
                
### Policy Implications
- Infrastructure upgrades such as traffic calming, protected bike lanes, and safer pedestrian crossings could address high-risk zones.
- Targeted enforcement during high-fatality time windows could reduce dangerous behaviour.
- Public awareness campaigns should focus on both drivers and vulnerable road users during peak months.

### Conclusion
The data shows clear, actionabble trends. Most fatalities follow patterns in time, location, and behaviour. these patterns provide crucial direction for Chicago's Vision Zero strategy. By focusing on the most impacted victim groups, times, and locations, the city can make meaningful progress toward its goal of eliminating traffic deaths entirely.
                """)