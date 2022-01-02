import os
import csv
import requests
from datetime import date
import private
appid = private.appid

def data_collection(cities):
    
    """
    Collects the city location and weather information.
    
    Takes as arguments:
    *cities : a list of city names
    
    Saves:
    *city_weather_data.csv: a csv file containing the city name, lat, lon, id and weather data for that city for the 7 upcoming days
    """
    
    #Erase the files from the previous call to this function in case they exist   
    filename = 'city_weather_data.csv'
    if filename in os.listdir('data_files/'):
        os.remove('data_files/' + filename) 
    
    #Create the writer object to write the dictionaries live after each loop save memory space
    with open('data_files/city_weather_data.csv', 'a', newline='') as csvfile:
        cols = ['city_id', 'date_updated', 'lat', 'lon', 'city_name', 'date', 'humidity', 'wind_sp', 'cloudiness', 'prob_preci', 'uv_index', 'day_temp', 'day_temp_feels', 'rain']
        writer = csv.DictWriter(csvfile, fieldnames=cols)
        writer.writeheader()

        for city in cities:

            c_request = requests.get('https://nominatim.openstreetmap.org/search?q={}&country=france&format=json'.format(city.replace(' ', '+')))
            c_data = c_request.json()[0]        
            c_keys = {'city_id':'place_id', 'lat' : 'lat', 'lon':'lon'} #keys of the information we are interested in in the json file
            c_info = {key: c_data[val] for key, val in c_keys.items()} #generate a dictionary of the desired city information
            c_info['city_name'] = city
            c_info['date_updated'] = date.today()

            w_request = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat={}&units=metric&lon={}&&exclude=current,minutely,hourly&appid={}' \
                                           .format(float(c_info['lat']), float(c_info['lon']), appid))

            w_data = w_request.json()['daily']

            for day in range(1, len(w_data)): #retrieve data for seven upcoming days starting tomorrow

                w_info = {}

                w_info.update(c_info)

                w_keys = {'date':'dt', 'humidity':'humidity', 'wind_sp':'wind_speed', 'cloudiness':'clouds', 'prob_preci':'pop', 'uv_index':'uvi'} #keys for which data can be retrieved easily
                w_info.update({key: w_data[day][value] for key, value in w_keys.items()})

                w_info.update({'day_temp': w_data[day]['temp']['day']}) #returns temps for the 'day'th day from request
                w_info.update({'day_temp_feels' : w_data[day]['feels_like']['day']}) #returns felt temps for the 'day'th day from request

                try:

                    w_info.update({'rain': w_data[day]['rain']}) # if rain is forecasted will find rain info otherwise nothing there

                except KeyError:

                    w_info.update({'rain': 0}) # if doesn't find rain info just puts a 0
            

                writer.writerow(w_info)
            
            