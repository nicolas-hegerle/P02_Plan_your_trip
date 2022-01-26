# run this script to update the data

# import the necessary libraries
import time
from scrap_hotels import Scrap_hotel_info


# use of personal token for weather info
import private
appid = private.appid

# import pyton scripts
from collect_city_weather_data import data_collection
from compute_winner import compute_winners
from scrap_hotels import hotel_scraper

print("====Finished importing the required packages libraries====\n")

# list of the 35 best places to visit in france according to https://one-week-in.com/35-cities-to-visit-in-france

cities = ["Mont Saint Michel", "St Malo", "Bayeux", "Le Havre", "Rouen", "Paris", "Amiens",
"Lille", "Strasbourg", "Chateau du Haut Koenigsbourg", "Colmar", "Eguisheim", "Besancon", "Dijon",
"Annecy", "Grenoble", "Lyon", "Gorges du Verdon", "Bormes les Mimosas", "Cassis", "Marseille",
"Aix en Provence", "Avignon", "Uzes", "Nimes", "Aigues Mortes", "Saintes Maries de la mer",
"Collioure", "Carcassonne", "Ariege", "Toulouse", "Montauban", "Biarritz", "Bayonne",  "La Rochelle"]


# retrieve city and weather info. Will save the data automatically
print(f"====Started collecting city and weather information at {time.strftime('%Y-%m-%d %H:%M:%S')}====\n")
data_collection(cities)
print(f"====Finished collecting city and weather information at {time.strftime('%Y-%m-%d %H:%M:%S')}====\n")


# scrap the hotel information from booking.com. Code last updated on 2022/01/02
# scraps top 100 hotels for the 35 best places in France

scrapper = Scrap_hotel_info
crawler = hotel_scraper()

print(f"====Started scrapping hotel information at {time.strftime('%Y-%m-%d %H:%M:%S')}====")
print("---This usually takes about 30 minutes---\n")
crawler.crawl(scrapper)
crawler.start()
print(f"====Finished scrapping hotel information at {time.strftime('%Y-%m-%d %H:%M:%S')}====\n")
print("****DATA UPDATED SUCCESSFULLY****")
