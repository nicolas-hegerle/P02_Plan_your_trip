import pandas as pd
from datetime import datetime
import os

def compute_winners(importance, nb_cities=5):
    """
    Retrieves the date from the weather data collection and computes the 'winners' table.
    
    Takes as arguments:
    *importance: a dictionarie containing the relative importance for the following weather features:
        -humidity, wind_sp, cloudiness, uv_index, day_temp, day_temp_feels, rain
    *top: the proportion of cities you want to return Ex: 0.25 will return 1/4th of the cities in the list
    
    Returns:
    This function returns a dataframe containing the information of the winnign cities
    """
    #Erase the files from the previous call to this function in case they exist   
    filenames = ['city_weather_score.csv', 'top_cities.csv']
    for file in filenames:
        if file in os.listdir('data_files/'):
            os.remove('data_files/' + file)


    #Read data from the csv file, stores in in a pd.DataFrame and formats the date, lat and lon dtypes
    df_c_w_data = pd.read_csv("data_files/city_weather_data.csv")
    df_c_w_data = df_c_w_data.astype({'lat':'float64', 'lon':'float64'})
    df_c_w_data['date'] = df_c_w_data['date'].apply(lambda x : datetime.fromtimestamp(x).date())
    
    #List of weather features used to compute the city score
    weather_features = ['humidity', 'wind_sp', 'cloudiness', 'uv_index', 'day_temp', 'day_temp_feels', 'rain']
    
    #Generates a dictionary containing the dates as keys and the max value for each feature contained in a dictionary as values.
    #Used for normalising the values. Ex: dict = {date : {weather_features : max_per_date}}
    max_per_date = df_c_w_data.groupby('date')[weather_features].max().to_dict(orient='index')

    #Normalizes the values for each weather features per day and calculate the city score using the relative importance for each feature.
    #The normalized feature is obtained by deviding the value by the max value for a given date
    #The score is obtained by multiplying the normalized feature value by its relative importance (except for the rain feature. See below)
    #The city score is obtained by summing all the scores
    
    for row in df_c_w_data.index: #loops through all the rows of the dataframe
        
        city_score = 0 #variable to compute the city score on the fly
        
        for timestamp in max_per_date.keys(): #loops through the keys of the dictionary. Keys = timestamps
            
            if df_c_w_data.loc[row,'date'] == timestamp: #checks that dates match between key and date columns
                
                for feature, value in max_per_date[timestamp].items(): #loops through key, value pairs of the max_per_date dictionary values
                    
                        if max_per_date[timestamp][feature] == 0: #since we kept the max values, if the max is 0 all values for that day are 0
                            df_c_w_data["rel_" + feature] = 0
                            
                        elif feature == 'rain': #the rain score is calculated by using the pop * the normalized rain * importance factor
                            df_c_w_data.loc[row,"rel_" + feature] = \
                            df_c_w_data.loc[row, feature] / max_per_date[timestamp][feature] * importance[feature] * df_c_w_data.loc[row,'prob_preci']
                        
                        else:  
                            df_c_w_data.loc[row,"rel_" + feature] = \
                            df_c_w_data.loc[row, feature] / max_per_date[timestamp][feature] * importance[feature]
                        
                        city_score += df_c_w_data.loc[row,"rel_" + feature] #computes the city score by summing each score
                df_c_w_data.loc[row, 'score'] = city_score #stores the score in the data frame at the given row => one score per date
    
    total_score = df_c_w_data.groupby('city_name', as_index=False)['score'].sum().rename(columns={'score':'score_total'}) #calculates the total score for each ctity
    avg_scores = df_c_w_data.groupby('city_name', as_index=False)[['humidity', 'wind_sp', 'cloudiness', 'uv_index', 'day_temp', 'day_temp_feels', 'rain', 'score']].mean() #calculates the average score per weather feature for each city
    
    #Generate the dataframe with all the city scores and weather information for each date
    df_city_score_data = df_c_w_data \
                        .merge(avg_scores, how='left', on='city_name', suffixes = ('_daily', '_avg')) \
                        .merge(total_score, how='left', on='city_name') 
   
    #Generate the top cities dataframe based on their score
    top_cities = total_score.nlargest(nb_cities, 'score_total', keep='all')
    df_top_cities = df_c_w_data.groupby('city_name', as_index=False).mean().rename(columns={'score':'score_avg'}) \
                    .merge(top_cities, how='right', on ='city_name')
    
    #Save the dataframe to a csv
    df_city_score_data.to_csv(r'data_files/city_weather_score.csv') #saves the city score data df to a csv file
    df_top_cities.to_csv(r'data_files/top_cities.csv') #saves the top cities df to a csv file
    

    print("\nBased on your preferences the top {} cities to travel to over the next 7 days seem to be:\n{}".format(nb_cities, top_cities['city_name'].to_string(index=False)))
       
    return df_city_score_data, df_top_cities  
    