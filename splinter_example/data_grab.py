from splinter import Browser
import pandas as pd
import json
from datetime import datetime
from pytz import timezone
from grab_funcs import *

# Read in json
with open('config.json') as fp:
    config = json.load(fp)

# Get the current time
tz = timezone(config['timezone'])
day = datetime.now(tz).date()

browser = Browser('chrome')

info = pd.DataFrame(columns=['day', 'company', 'product', 'price'])

for product in config['products']:
    browser.visit(product['url'])

    if 'type_tag' in product:
        info = info.append(purple_mattress_pricing(browser, product['url'], product['size_tag'], product['size_selector'], product['product_name'], day, product['price_tag'], product['price_selector'], config['close_tags'], type_tag=product['type_tag'], type_selector=product['type_selector']))
    else:
        info = info.append(purple_mattress_pricing(browser, product['url'], product['size_tag'], product['size_selector'], product['product_name'], day, product['price_tag'], product['price_selector'], config['close_tags']))

browser.quit()

print(info)
