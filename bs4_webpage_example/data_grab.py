################################################################################
# Script using BeautifulSoup to grab pricing data from another website specified
# by config.json
################################################################################

# Change os directory to correct directory
import os
# If running locally
#dirr = '/Users/zachparis/Documents/coffee_and_code/bs4_webpage_example

dirr = os.path.dirname(os.path.realpath(__file__)) # this automatically gets the directory of the running file
os.chdir(dirr)

from grab_func import casper_assorted_pricing
import json
import pandas as pd
from datetime import datetime
from pytz import timezone

# Read in json file
with open('config.json') as fp:
    config = json.load(fp)

# Get current date in specified timezone
tz = timezone(config['timezone'])
day = datetime.now(tz).date()

# Create a DataFrame instance to hold data
info = pd.DataFrame(columns=['day', 'company', 'product', 'price'])

# Iterate through listed products and append to DataFrame
for product in config['products']:
    info = info.append(casper_assorted_pricing(product['url'], product['product_name'], product['price_selector'], product['price_tag'], day), ignore_index=True)

print(info)
