#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Connect to browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    try:
        # Find the article title
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Find the plain text article summary
        news_summary = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_summary

def featured_image(browser):
    # Visit new url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find "Full Image" Button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Connect BSoup to new website
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Get the partial URL
        img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
        img_url_rel
    except AttributeError:
        return None

    # Complete the URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    try:
        # Set table to Pandas DataFrame
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of DataFrame
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace = True)

    # Set DataFrame to easy-access HTML
    df.to_html()

# End remote browser
browser.quit()