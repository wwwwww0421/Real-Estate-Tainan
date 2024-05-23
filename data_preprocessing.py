import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math


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
