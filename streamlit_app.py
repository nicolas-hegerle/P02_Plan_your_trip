# import the necessary libraries

import streamlit as st

import pandas as pd
import numpy as np


import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

from compute_winner import compute_winners

st.set_page_config(layout="wide")

# variables used in the app

df_top_cities = pd.DataFrame()

default_cities = ["Mont Saint Michel", "St Malo", "Bayeux", "Le Havre", "Rouen", "Paris", "Amiens",
"Lille", "Strasbourg", "Chateau du Haut Koenigsbourg", "Colmar", "Eguisheim", "Besancon", "Dijon",
"Annecy", "Grenoble", "Lyon", "Gorges du Verdon", "Bormes les Mimosas", "Cassis", "Marseille",
"Aix en Provence", "Avignon", "Uzes", "Nimes", "Aigues Mortes", "Saintes Maries de la mer",
"Collioure", "Carcassonne", "Ariege", "Toulouse", "Montauban", "Biarritz", "Bayonne",  "La Rochelle"]

weather_features = {
    'humidity' : "Percent (%) humidity", \
    'wind_sp' : "Forcasted wind speed in metre/sec", \
    'cloudiness' : "Score of forcasted cloudiness", \
    'uv_index' : 'Forcasted UV index', \
    'day_temp' : 'Forcasted temperature during the day in °C', \
    'day_temp_feels': 'Forcasted felt temperature during the day in °C', \
    'rain' : 'Forcasted probability of precipitation'
            }

rel_importance = {}

# prepare the sidebar options

st.sidebar.subheader("Select number of top locations to return:")

nb_cities = st.sidebar.slider(
        label = "# cities to return",
        min_value=1,
        max_value=len(default_cities),
        step=1,
        value = 5,
        key = 'nb_cities', 
        help = 'Select the number of locations you want the app to return based on the weather info score calculation'
    )

st.sidebar.subheader("Specifiy your weather preferences:")

for feature, help in weather_features.items():
    globals()[feature] = st.sidebar.slider(
        label = feature.title(),
        min_value=1.0,
        max_value=2.0,
        step=0.1,
        value = 1.0,
        key = feature, 
        help = help
    )

    globals()["neg_"+feature] = st.sidebar.checkbox(
        label = feature.title() + ' negatively impacts decision',
        key = 'neg'+feature
    )

    if globals()["neg_"+feature.lower()]:
        globals()[feature] = globals()[feature] * -1

    rel_importance[feature] = globals()[feature.lower()]

get_top_cities = st.sidebar.button(
                        label = 'Get info',
                        key = 'compute_top_cities',
                        help = 'click the button to retrieve your top {} locations based on your preferences'.format(nb_cities),
                    )

display_importance = pd.DataFrame(data = rel_importance, columns = rel_importance.keys(), index = ['Values'])


if get_top_cities:
    _, df_top_cities = compute_winners(rel_importance, nb_cities)
    
if df_top_cities.shape[0] != 0:
    # get the hotels for those cities
    df_all_hotels = pd.read_json("data_files/city_hotels.json", encoding='utf-8')
    mask = pd.Series([True if (city in df_top_cities['city_name'].tolist()) else False for city in df_all_hotels['location']])
    df_top_city_hotels = df_all_hotels.loc[mask]

    # plot the top cities on a map
    hover_show_city = ['score_total', 'day_temp_feels', 'rain', 'uv_index']
    hover_data_city = {col:True if col in hover_show_city else False for col in df_top_cities.columns}

    center_lat_city = df_top_cities['lat'].mean()
    center_lon_city = df_top_cities['lon'].mean()
    center_city = {'lat' : center_lat_city, 'lon' : center_lon_city}

    plot_cities = px.scatter_mapbox(
        df_top_cities, 
        lat = 'lat', 
        lon = 'lon', 
        color = 'day_temp_feels', 
        size = 'day_temp', 
        zoom = 4, 
        mapbox_style='carto-positron', 
        width=700,
        height=600, 
        hover_name = 'city_name', hover_data = hover_data_city, 
        center = center_city
)

   
    # plot hotels for the top cities
    hover_show_hotel = ['location', 'hotel_score', 'score_title', 'score_expe', 'url']
    hover_data_hotel = {col:True if col in hover_show_hotel else False for col in df_top_city_hotels.columns}

    center_lat_hotel = df_top_city_hotels['hotel_lat'].mean()
    center_lon_hotel = df_top_city_hotels['hotel_lon'].mean()
    center_hotel = {'lat' : center_lat_hotel, 'lon' : center_lon_hotel}

    plot_hotels = px.scatter_mapbox(
            df_top_city_hotels,
            lat = "hotel_lat", 
            lon = "hotel_lon", 
            color = 'hotel_score', 
            zoom = 4, 
            mapbox_style="carto-positron", 
            width=700, 
            height=600, 
            hover_name = "hotel_name", 
            hover_data=hover_data_hotel, 
            center = center_hotel,
    )


# build the webpage

header = st.container()
description = st.expander(label = 'How to:', expanded = False)
winners = st.container()
city_hotel_plots = st.container()
hotel_links = st.container()

with header:
    st.title("Prepare your trip with our awsome app")
    st.text("Find out where you should head to among 35 best places to visit in France")

with description:
    st.markdown(
        "This page allows to set your weather preferences and compute the top locations to travel to over the next 7 days.<br>\
        Locations include **35 top destinations to visit in France** based on <a href='https://one-week-in.com/35-cities-to-visit-in-france/' target='_blank'><br>\
        Use the sliders and checkboxes in the sidebar to set the factor applied to your weather score.<br>\
        You want a place with a lot of wind because you like having a nice breeze in your face. Notch the <ins>wind_sp</ins> factor up to 2.<br>\
        Rain is definitely a no-go for you. Set the factor to be negative by ticking <ins>rain negatiely impacts decision</ins> box.<br>\
        Then just click the button and get your cities and hotels.",
        unsafe_allow_html=True
    )

with winners:
    st.subheader("Selected weather feature relative importance:")
    st.write(display_importance)
    if df_top_cities.shape[0] != 0:
        top_cities = [city for city in df_top_cities['city_name']]
        st.subheader(f"Top {nb_cities} cities to travel to in the next 7 days")
        st.text(f'Note: data last update on {df_top_city_hotels["date_updated"].unique()[0]}')
        st.write('Based on your preferences the top cities to travel to are : {}'.format(str(top_cities).strip("[]").replace("'", "")))
        to_show = ['city_name', 'score_total'] + list(weather_features.keys())
        st.write(df_top_cities[to_show])

with city_hotel_plots:
    city_plot, hotel_plot = st.columns(2)

    if df_top_cities.shape[0] != 0:
        city_plot.subheader(f"Top {nb_cities} locations based on you preferences")
        city_plot.plotly_chart(plot_cities, use_container_width=True)

        hotel_plot.subheader(f"Top hotels for those destinations")
        hotel_plot.plotly_chart(plot_hotels, use_container_width=True)

with hotel_links:
    if df_top_cities.shape[0] != 0:
        st.header("Hotel information and links")
        cols_to_show = ['location', 'hotel_name', 'hotel_score', 'score_title', 'score_expe', 'url']
        st.write(df_top_city_hotels[cols_to_show])









