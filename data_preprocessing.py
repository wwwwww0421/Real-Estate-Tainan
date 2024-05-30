import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import requests


apikey = open("api_key.txt", "r")
district_string = "東區、中區、西區、南區、北區、安平區、安南區、新營區、永康區、鹽水區、白河區、麻豆區、佳里區、新化區、善化區、學甲區、柳營區、後壁區、東山區、下營區、六甲區、官田區、大內區、西港區、七股區、將軍區、北門區、新市區、安定區、山上區、玉井區、楠西區、南化區、左鎮區、仁德區、歸仁區、關廟區、龍崎區"
district_lst = district_string.split("、")


def get_land_size(size):
    return round(float(str(size).split()[0]), 2)


def get_land_price(price):
    return extract_numerical_part(price)


def extract_numerical_part(string):
    numerical_part = "".join([char for char in string if char.isdigit()])
    if numerical_part == "":
        return np.nan
    else:
        return float(numerical_part)


def remove_special_characters(string):
    special_characters = "/\@$£%@$^"
    pattern = f"[{re.escape(special_characters)}]"
    return re.sub(pattern, "", string)


def get_house_price(price):
    single_or_total = ["坪", "平"]
    price = str(price)
    if price == "0":
        return np.nan, np.nan
    elif remove_special_characters(price.split("萬")[1]) in single_or_total:
        if len(price.split("萬")[0].split("~")) == 1:
            return extract_numerical_part(price.split("萬")[0]), np.nan
        else:
            return extract_numerical_part(
                price.split("萬")[0].split("~")[0]
            ), extract_numerical_part(price.split("萬")[0].split("~")[1])
    else:
        if len(price.split("萬")[0].split("~")) == 1:
            return extract_numerical_part(price.split("萬")[0]), np.nan
        else:
            return extract_numerical_part(
                price.split("萬")[0].split("~")[0]
            ), extract_numerical_part(price.split("萬")[0].split("~")[1])


def get_house_size(size):
    if len(size.split("~")) == 1:
        return extract_numerical_part(size[0]), np.nan
    else:
        return extract_numerical_part(size.split("~")[0]), extract_numerical_part(
            size.split("~")[1]
        )


def get_avg(mini, maxi):
    avg = (mini + maxi) / 2
    if pd.isna(avg) == True:
        return 0
    else:
        return avg


def check_string_in_list(string, lst):
    for element in lst:
        if element in string:
            return element
    return None


def get_district(location):
    if "區" in str(location):
        return check_string_in_list(str(location), district_lst)
    else:
        return np.nan


def get_plotable_range(data):
    plotable_house = data[
        (data.latitude >= 22.894)
        & (data.latitude <= 23.412)
        & (data.longitude >= 120.036)
        & (data.longitude <= 120.656)
    ]
    return plotable_house


def get_lat_lon(address):
    # Initialize Nominatim API

    # Replace YOUR_API_KEY with your actual API key. Sign up and get an API key on https://www.geoapify.com/
    API_KEY = "cf78f92dd910429c821d49d6863ef6bf"

    # Build the API URL
    url = f"https://api.geoapify.com/v1/geocode/search?text={address}&limit=1&apiKey={API_KEY}"

    # Send the API request and get the response
    response = requests.get(url)

    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()
        try:
            # Extract the first result from the data
            result = data["features"][0]

            # Extract the latitude and longitude of the result
            latitude = result["geometry"]["coordinates"][1]
            longitude = result["geometry"]["coordinates"][0]

            print(f"Latitude: {latitude}, Longitude: {longitude}")
            return latitude, longitude
        except:
            return np.nan, np.nan
    else:
        print(f"Request failed with status code {response.status_code}")
        return np.nan, np.nan


def data_processing_land(data):

    data["district"] = data.apply(lambda x: get_district(x["位置"]), axis=1)

    data = data.fillna(0)
    data["avg_size"] = data["坪數"].apply(get_land_size)
    data["avg_price"] = data["開價"].apply(extract_numerical_part)

    return data


def data_processing_house(data):

    data = data.fillna(0)
    data["min_price"] = data.apply(lambda x: get_house_price(x["總價"])[0], axis=1)
    data["max_price"] = data.apply(lambda x: get_house_price(x["總價"])[1], axis=1)

    data["min_size"] = data.apply(lambda x: get_house_size(x["格局/地坪"])[0], axis=1)
    data["max_size"] = data.apply(lambda x: get_house_size(x["格局/地坪"])[1], axis=1)

    data["district"] = data.apply(lambda x: get_district(x["位置"]), axis=1)

    data = data.fillna(0)
    data["avg_size"] = data.apply(lambda x: get_avg(x.min_size, x.max_size), axis=1)
    data["avg_price"] = data.apply(lambda x: get_avg(x.min_price, x.max_price), axis=1)
    return data
