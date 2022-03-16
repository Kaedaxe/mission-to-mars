#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# Find the article title
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Find the article summary
slide_elem.find('div', class_='article_teaser_body')

news_summary = slide_elem.find('div', class_='article_teaser_body').get_text()
news_summary


# ### Featured Images

url = 'https://spaceimages-mars.com'
browser.visit(url)

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

html = browser.html
img_soup = soup(html, 'html.parser')

img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
img_url_rel

img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace = True)
df

df.to_html()

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

for i in range(0, 4):
    # Refresh hemispheres dictionary
    hemispheres = {}
    
    # Click current link
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    img_dnld = browser.links.find_by_partial_text('Enhanced')[i]
    img_dnld.click()

    # Find .jpg image
    html = browser.html
    wide_img_soup = soup(html, 'html.parser')
    img_jpg = wide_img_soup.find('img', class_ = 'wide-image').get('src')
    img_url = f'https://marshemispheres.com/{img_jpg}'
    
    # Find the image title and set the hemisphere dictionary
    title = wide_img_soup.find('h2', class_ = 'title').get_text()
    hemispheres = {'img_url':img_url, 'title':title}
    
    # Add Dictionary to List
    hemisphere_image_urls.append(hemispheres)
    
    # Navigate back to the main page
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()




