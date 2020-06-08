# scrape_mars.py by Preston Hinkel
import time
import pandas as pd
import requests
import json
import datetime as dt
import re
from splinter import Browser
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

def scrape():

    # Creating the browser to scrape with
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Giving the web path to the site we are scraping
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(2)
    # Iterate through all pages
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    browser.quit()

    title = soup.select('.content_title')[1]
    description = soup.select('.article_teaser_body')[0]
    title = re.sub('<.*>','',title.text)
    description = re.sub('<.*>','',description.text)

    # Creating the browser to scrape with
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Giving the web path to the site we are scraping
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)
    # Iterate through all pages
    html = browser.html
    soup = BeautifulSoup(html, 'html')
    browser.quit()

    test = soup.find_all('section')
    imageurl = test[1].find('footer').find('a').attrs['data-fancybox-href']
    imageurl = "https://www.jpl.nasa.gov" + imageurl

    mars_weather = "This information is currently unavailable from Twitter, so I guess we will just see when we get there."

    # Creating the browser to scrape with
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Giving the web path to the site we are scraping
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(2)
    # Iterate through all pages
    html = browser.html
    soup = BeautifulSoup(html, 'html')
    browser.quit()

    test = soup.select('.textwidget')
    rowlist = test[1].find_all("tr")
    newrowlist = []
    for row in rowlist:
        newrowlist.append(row.text)
    rowlist = []
    for row in newrowlist:
        rowlist.append(row.split(':'))

    factFrame = pd.DataFrame(rowlist, columns = ['Description', 'Value'])
    html_facts = factFrame.to_html()

    # Creating the browser to scrape with
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Giving the web path to the site we are scraping
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)
    # Iterate through all pages
    html = browser.html
    soup = BeautifulSoup(html, 'html')
    browser.quit()

    listtest = soup.find_all("a")
    betterlist = []
    for item in listtest:
        try:
            if item.attrs["class"] != ['icon']:
                betterlist.append(item)
        except:
            pass

    x = 0
    better_dict = {}
    while x < 7:
        better_dict[betterlist[1+x].text] = "https://astropedia.astrogeology.usgs.gov" + betterlist[0+x]["href"].replace("/search/map/", "/download/") + ".tif/full.jpg"
        x = x + 2

    dict_return = {"article_title" : title, "article_description" : description, "featured_image" : imageurl, "weather_report" : mars_weather, "fact_table" : html_facts, "hemispheres" : better_dict, "CerberusHemisphereEnhanced" : better_dict['Cerberus Hemisphere Enhanced'], "SchiaparelliHemisphereEnhanced" : better_dict['Schiaparelli Hemisphere Enhanced'], "SyrtisMajorHemisphereEnhanced" : better_dict['Syrtis Major Hemisphere Enhanced'], "VallesMarinerisHemisphereEnhanced" : better_dict['Valles Marineris Hemisphere Enhanced']}

    return dict_return

print(scrape())