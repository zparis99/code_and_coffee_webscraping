from urllib import request
from bs4 import BeautifulSoup as bs
import pandas as pd

# Remove comma and dollar sign if it exists from price and cast to int
def clean_price(text):
    if '.' in text:
        text = text[:text.find('.')]

    return int(text.replace(',', '').replace('$', ''))

def casper_assorted_pricing(url, product, price_selector, price_tag, today):
    # Create soup
    soup = bs(request.urlopen(url), 'lxml')
    price = clean_price(soup.select(price_tag+price_selector)[0].string)

    temp = pd.Series(index=['day', 'company', 'product', 'price'])
    # Add and return data
    temp.loc['day'] = today
    temp.loc['company'] = 'Casper'
    temp.loc['product'] = product
    temp.loc['price'] = price

    return temp
