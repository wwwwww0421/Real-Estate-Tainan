import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import requests


apikey = open("api_key.txt", "r")


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
    data["size"] = data["坪數"].apply(get_land_size)
    data["price"] = data["開價"].apply(extract_numerical_part)
    return data


def data_processing_house(data):
    data = data.fillna(0)
    data["min_price"] = data.apply(lambda x: get_house_price(x["總價"])[0], axis=1)
    data["max_price"] = data.apply(lambda x: get_house_price(x["總價"])[1], axis=1)
    data["min_size"] = data.apply(lambda x: get_house_size(x["格局/地坪"])[0], axis=1)
    data["max_size"] = data.apply(lambda x: get_house_size(x["格局/地坪"])[1], axis=1)
    return data
