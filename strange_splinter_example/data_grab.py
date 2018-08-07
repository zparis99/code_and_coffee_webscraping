################################################################################
# Script to demonstrate that no two websites are the same and you sometimes have
# to work in less conventional ways.
################################################################################

import os
# If running locally
#dirr = '/Users/zachparis/Documents/coffee_and_code/strange_splinter_example'

dirr = os.path.dirname(os.path.realpath(__file__)) # this automatically gets the directory of the running file
os.chdir(dirr)

from splinter import Browser
import json
import pandas as pd
from datetime import datetime
from pytz import timezone
from grab_funcs import tnn_assorted_pricing

# Read in config file
with open('config.json') as fp:
    config = json.load(fp)

# Get current date in timezone specified in config file
tz = timezone(config['timezone'])
day = datetime.now(tz).date()

# Open Chrome browser
browser = Browser('chrome')

# Create empty dataframe to hold information
info = pd.DataFrame(columns=['day', 'company', 'product', 'price'])

for product in config['products']:
    info = info.append(tnn_assorted_pricing(browser, product['url_list'], product['broad_product'], product['product_list'], product['price_tag'], product['price_selector'], day))

# Quit browser
browser.quit()

print(info)

# Store dataframe in excel file
info.to_excel('tnn_pricing.xlsx')
