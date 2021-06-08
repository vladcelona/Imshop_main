from web import *
from bs4 import BeautifulSoup as bs
from web import Web as web_
import os, sys
import requests
import pandas as pd

# The url of the website that I need to parse, so...
# Changed it a little bit, so now I can work with all reviews
url_main = 'https://apps.shopify.com/plobalapps-mobile-application/reviews'

# This variable is need to see if the code needs to create table or not
global_parameter = True
columns = ['Replier', 'Rating', 'Date of reply', 'Description']
dict_columns = {columns[0]: [], columns[1]: [], columns[2]: [], columns[3]: []}


def get_class_or_tag():
    code = requests.get(url_main)
    soup_code = bs(code.text, 'html.parser')
    print(soup_code.select_one('span[class^="review-listing-header__text"]').text)


def table_data():
    global global_parameter, dict_columns
    if global_parameter:
        default_data = pd.DataFrame(data=dict_columns, index=columns).T
        default_data.to_csv("reply_database.csv")
    else:
        reply_data = pd.read_csv("reply_database.csv")
        return reply_data


def parse_url():
    website_code = web_(url_main).get_code()
    print(website_code)

# parse_url()
get_class_or_tag()