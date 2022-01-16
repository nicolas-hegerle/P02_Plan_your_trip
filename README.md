# Plan your trip with Kayak 

**<font size = 6>Visit the app at https://share.streamlit.io/nicolas-hegerle/p02_plan_your_trip/main</font>**

## Project 🚧

The marketing team needs help on a new project. After doing some user research, the team discovered that **70% of their users who are planning a trip would like to have more information about the destination they are going to**. 

In addition, user research shows that **people tend to be defiant about the information they are reading if they don't know the brand** which produced the content. 

Therefore, Kayak Marketing Team would like to create an application that will recommend where people should plan their next holidays. The application should be based on real data about:

* Weather 
* Hotels in the area 

The application should then be able to recommend the best destinations and hotels based on the above variables at any given time. 

## Goals 🎯

As the project has just started, your team doesn't have any data that can be used to create this application. Therefore, your job will be to: 

* Scrape data from destinations 
* Get weather data from each destination 
* Get hotels' info about each destination
* Store all the information above in a data lake
* Extract, transform and load cleaned data from your datalake to a data warehouse

## Scope of this project 🖼️

Marketing team wants to focus first on the best cities to travel to in France. According <a href="https://one-week-in.com/35-cities-to-visit-in-france/" target="_blank">One Week In.com</a> here are the top-35 cities to visit in France: 

```python 
["Mont Saint Michel",
"St Malo",
"Bayeux",
"Le Havre",
"Rouen",
"Paris",
"Amiens",
"Lille",
"Strasbourg",
"Chateau du Haut Koenigsbourg",
"Colmar",
"Eguisheim",
"Besancon",
"Dijon",
"Annecy",
"Grenoble",
"Lyon",
"Gorges du Verdon",
"Bormes les Mimosas",
"Cassis",
"Marseille",
"Aix en Provence",
"Avignon",
"Uzes",
"Nimes",
"Aigues Mortes",
"Saintes Maries de la mer",
"Collioure",
"Carcassonne",
"Ariege",
"Toulouse",
"Montauban",
"Biarritz",
"Bayonne",
"La Rochelle"]
```

Focus **only on the above cities for this project**. 

## Results and available data/document

### Weather data

* Weather data were retrieved using city geo coordinates obtained on https://nominatim.org/ and the openweathermap API https://openweathermap.org/appid.

* ```collect_city_weather_data.py``` holds the function used to retrieve this information and save it in a csv file

* ```compute_winner.py``` is used to calculate the top cities based on user's weather preferences

### Hotel data 

* Hotel information is scrapped from booking.com using scrapy.

* ```scrap_hotels.py``` holds the function used to retrieve hotel information and store it in a csv file 

### Updating and showing data

* ```update_data.py``` can be ran to update the weather and hotel data, usually takes around 30 minutes to update. Files are saved automatically

* ```P02_Plan_Your_trip.ipynb``` displays info and enables to see results in a notebook as well as send data to AWS S3 and RDS PostGreSQl db

* ```streamlit.app``` is used by streamlit along with the ```requirements.txt``` to build the webpage that allows user to play around with weather data and get result for the top cities.<br>
Visit the app at https://share.streamlit.io/nicolas-hegerle/p02_plan_your_trip/main

 
