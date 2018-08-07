###############################################################################
# Basic data grab from a webpage using bs4, end goal is to grab the from the
# first paragraph of basic_css_example.html
################################################################################

from bs4 import BeautifulSoup
import os
# If running locally
#dirr = '/Users/zachparis/Documents/coffee_and_code/basic_bs4_example'
dirr = os.path.dirname(os.path.realpath(__file__)) # this automatically gets the directory of the running file
os.chdir(dirr)

# Load html file into BeatifulSoup instance
with open('./page_files/basic_css_example.html') as fp:
    soup = BeautifulSoup(fp, 'lxml')

# Print out a text representation of the html file
print("PAGE HTML:")
print(soup)

# Find div with id=main
soup.find(id='main')

# Find tag with class blue
soup.find(class_='blue')

# Find all tags with class red
red = soup.find_all(class_='red')

# Narrow down to just paragraph tag
for tag in red:
    if tag.name == 'p':
        print("TEXT:", tag.string)
        break
