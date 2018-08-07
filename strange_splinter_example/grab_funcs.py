import pandas as pd
import time

# Remove comma and dollar sign if it exists from price and cast to int
def clean_price(text):
    if '.' in text:
        text = text[:text.find('.')]

    return int(text.replace(',', '').replace('$', ''))


def tnn_assorted_pricing(browser, url_list, broad_product, product_list, price_tag, price_selector, today):
    # Store information in DataFrame
    info = pd.DataFrame(columns=['day', 'company', 'product', 'price'])

    for url in url_list:
        browser.visit(url)

        # Add info to series then append to DataFrame
        temp = pd.Series(index=['day', 'company', 'product', 'price'])
        temp.loc['day'] = today
        temp.loc['company'] = 'Tuft & Needle'
        temp.loc['product'] = broad_product + ' ' + product_list[url_list.index(url)]
        # Wait to give it time to load by ensuring price is an int
        while type(temp.loc['price']) != int:
            for price in browser.find_by_css(price_tag + price_selector):
                # Get past the extra price tags
                if price.text != '':
                    temp.loc['price'] = clean_price(price.text)

        info = info.append(temp, ignore_index=True)

    return info
