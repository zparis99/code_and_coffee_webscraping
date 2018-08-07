import pandas as pd
from splinter.exceptions import ElementDoesNotExist
from selenium.common.exceptions import WebDriverException

# Remove comma and dollar sign if it exists from price and cast to int
def clean_price(text):
    if '.' in text:
        text = text[:text.find('.')]

    return int(text.replace(',', '').replace('$', ''))

# Grab Purple price
def purple_price_grab(browser, price_tag, price_selector):
    # Return price
    return clean_price(browser.find_by_css(price_tag + price_selector).text)

# Create Purple Series
def purple_series(browser, broad_product, price_tag, price_selector, today, size=None, type=None):
    # Grab info and add to Series
    temp = pd.Series(index=['day', 'company', 'product', 'price'])
    temp.loc['day'] = today
    temp.loc['company'] = 'Purple'
    if size is None and type is None:
        temp.loc['product'] = broad_product
    elif size is not None and type is None:
        temp.loc['product'] = broad_product + ' ' + size
    else:
        temp.loc['product'] = broad_product + ' ' + size + ' ' + type
    temp.loc['price'] = purple_price_grab(browser, price_tag, price_selector)

    return temp

# Will click through options on purple webpage to grab pricing. Contains multiple
# try and except clauses in the event popups appear.
# browser is a Browser instance from splinter
# url is the url of the page
# size_tag is the tag type i.e. 'div' for the buttons which determine mattress size
# size_selector is the css selector for the size, all buttons should share a common class
# broad_product is the broad name of the product
# price_tag is the tag type i.e. 'div' for the tag holding the price
# price_selector is the selector for the price
# close_tags are the selectors [in a list] for the x-out buttons on popups
# type_tag is the tag for the type of mattress if present
# type_selector is the css selector for the types
def purple_mattress_pricing(browser, url, size_tag, size_selector, broad_product, today, price_tag, price_selector, close_tags, type_tag=None, type_selector=None):
    browser.visit(url)

    # Used to store mattress information
    info = pd.DataFrame(columns=['day', 'company', 'product', 'price'])

    # Iterate through size variants
    for size in browser.find_by_css(size_tag + size_selector):
        while True:
            try:
                # Click on size
                size.click()

                # If type is present, iterate
                if type_tag is not None:
                        for type in browser.find_by_css(type_tag + type_selector):
                            while True:
                                try:
                                    type.click()
                                    info = info.append(purple_series(browser, broad_product, price_tag, price_selector, today, size=size.text, type=type.text), ignore_index=True)
                                except:
                                    if all_popups(browser, ['close', 'modal-close-x']):
                                        continue
                                    else:
                                        break
                                else:
                                    break

                else:
                    info = info.append(purple_series(browser, broad_product, price_tag, price_selector, today, size=size.text), ignore_index=True)

            # If error is hit try closing**
            except Exception as e:
                print(e)
                # Try closing, if error is hit break from loop and move on
                if all_popups(browser, close_tags):
                    continue
                else:
                    break
            else:
                break

    return info

# Close multiple popus
def all_popups(browser, close_tags):
    if type(close_tags) != list:
        close_tags = [close_tags]
    for tag in close_tags:
        try:
            popup_close(browser, tag)
            print('Closed popup')
            return True
        except ElementDoesNotExist or WebDriverException:
            if close_tags.index(tag) == len(close_tags) - 1:
                print("Found no popups")
                return False
            pass

# Close popups with class of close_tag
def popup_close(browser, close_tag):
    browser.find_by_css(close_tag)[0].click()
