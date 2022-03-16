# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_all():
    # Initiate headless driver for
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemisphere_images": hemisphere_images(browser)
    }

    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemisphere_images(browser):
    url = 'https://marshemispheres.com/'
    # 1. Use browser to visit the URL
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for x in range(4):
        # Create empty dictionary for title, URL pairs
        hemispheres_x = {}
        # Creating path to each hemisphere's page and clicking the link to navigate to each page
        path = browser.find_by_tag('h3')[x].click()
        # Initializing splinter and URL references
        url = 'https://marshemispheres.com/'
        html = browser.html
        # Using Beautiful Soup to parse the resulting hemisphere pages' HTML
        image_soup = soup(html, 'html.parser')
        # Searching Soup HTML to find container for title and URL sections
        hemis = image_soup.find_all('div', class_="container")
        
        # Creating Try-Except section for collecting title and URL data and entering those into dictionary and list of each dict.
        try:
            for hemisphere in hemis:           
                image_path = hemisphere.select('li > a', limit=1)
                # For loop that removes the url information from the href section in the tag
                for link in image_path:
                    image = link['href']
                # Creating full URL for each image
                img_url = f'{url}{image}'
                # Grabbing each title relating to each hemisphere
                title = hemisphere.find('h2').get_text()
                hemispheres_x['img_url'] = img_url
                hemispheres_x['title'] = title
        except Exception as e:
            print(e)
        # Adding hemisphere dictionaries to list
        hemisphere_image_urls.append(hemispheres_x)
        # Browser returns to initial mars page for next iteration
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())