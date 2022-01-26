import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import os
import numpy as np
from datetime import date

cities = ["Mont Saint Michel", "St Malo", "Bayeux", "Le Havre", "Rouen", "Paris", "Amiens",
"Lille", "Strasbourg", "Chateau du Haut Koenigsbourg", "Colmar", "Eguisheim", "Besancon", "Dijon",
"Annecy", "Grenoble", "Lyon", "Gorges du Verdon", "Bormes les Mimosas", "Cassis", "Marseille",
"Aix en Provence", "Avignon", "Uzes", "Nimes", "Aigues Mortes", "Saintes Maries de la mer",
"Collioure", "Carcassonne", "Ariege", "Toulouse", "Montauban", "Biarritz", "Bayonne",  "La Rochelle"] 

max_offset = 75

class Scrap_hotel_info(scrapy.Spider):
        
        # Name of your spider that crawls all pages for each city
        name = "hotels_all_pages"

        # set the page offset to crawl through  hotels for a given city since we cannot follow page links so easily anymore
        city_offset = [{city:offset} for offset in np.arange(0,max_offset, 25) for city in cities]

        # Url to start your spider from 
        start_urls = [f"https://www.booking.com/searchresults.fr.html?&ss={next((i for i in co.keys()))}&nflt=ht_id%3D204%3B&order=class&offset={next((i for i in co.values()))}" for co in city_offset]

        # callback function called when the spider starts crawling. For each hotel on the page retrives the url of the hotel page
        def parse(self, response):
            
            hotels = response.css('div._fe1927d9e')
            
            for hotel in hotels:
                url = hotel.css('a.fb01724e5b').attrib['href']
                request = scrapy.Request(url, callback = self.parse_hotel_info, cb_kwargs = dict(location = response.url.split("&")[1].split('=')[1]))
                yield request
        
        # callbck function used to retrieve the information on the hotels using the hotel's url
        def parse_hotel_info(self, response, location):

            location = location.replace('%20', ' ')
            hotel_name = response.css('h2.hp__hotel-name::text').getall()[1].title().strip('\n').replace('%20', ' ')
            hotel_geo = response.css('p.address a.bui-link').attrib['data-atlas-latlng']
            hotel_lat = float(hotel_geo.split(",")[0])
            hotel_lon = float(hotel_geo.split(",")[1])
            hotel_score = response.css('div._9c5f726ff::text').get().replace(',', '.')
            score_expe = response.css('div._4abc4c3d5::text').get().split(' ')[0]
            hotel_link = response.url.split('?')[0]

            yield {
                'location' : location,
                'date_updated' : date.today(),
                'hotel_name' : hotel_name,
                'hotel_lat' : hotel_lat,
                'hotel_lon' : hotel_lon,
                'hotel_score' : hotel_score,
                'score_title' : response.css('div._192b3a196::text').get(),
                'score_expe' : score_expe,
                'url' : hotel_link
                        }

def hotel_scraper(filename = "city_hotels.json"):
    '''
    Function to scrap hotel info from booking for a list of cities passed as argument

    Arguments:
    cities: list, name of the locations you wish to get hotels for
    filename: string, name of the file the scrapped data will be saved to
    max_offset: int, used to scrap multiple pages for a same location on booking.com since following the link with scrapy is tedious.
    Offset of 0 returns the 25 best hotels for city, offset of 25 returns the 50 best hotels, etc... Offset of 75 returns 100 best hotels

    Returns:
    Scrap_hotel_info: the scrapy spider
    process: the crawler process

    To lauch the scrapper:
    scrapper, crawler = hotel_scraper([city, list], filename, max_offset = 75)
    crawler.crawl(scrapper)
    crawler.start()

    URL explained
    * full url: https://www.booking.com/searchresults.fr.html?&ss={}&nflt=ht_id%3D204%3B&order=class&offset={}
    * base domain: https://www.booking.com
    *first {}: replaced by the name of the city
    * second {}: replace by the offset
    * "&nflt=ht_id%3D204%3B": specifies you only want to retrieve hotels
    * "&order=class": sorts the results by decreasing score to the base domain
    * "&checkin_year=&checkin_month=&checkin_monthday=": can be used to specify desired dates of stay
    '''
    # Name of the file where the results will be saved
    filename = filename
    logs = 'log.txt'

    # If file already exists, delete it before crawling (because Scrapy will 
    # concatenate the last and new results otherwise)
    if filename in os.listdir('data_files/'):
        os.remove('data_files/' + filename)

    if logs in os.listdir('data_files/'):
        os.remove('data_files/' + logs)

    # Declare a new CrawlerProcess with some settings
    ## USER_AGENT => Simulates a browser on an OS
    ## LOG_LEVEL => Minimal Level of Log 
    ## FEEDS => Where the file will be stored 
    ## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
    process = CrawlerProcess(settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.231',
        'LOG_LEVEL': logging.INFO,
        'LOG_FILE' : "data_files/log.txt",
        'FEEDS': {
            'data_files/' + filename : {"format": "json"}, 
        },
        "AUTOTHROTTLE_ENABLED": True,
        "CONCURRENT_REQUESTS" : 5,
    })

    return process
