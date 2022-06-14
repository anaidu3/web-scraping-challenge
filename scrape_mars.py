# Automates browser actions
from splinter import Browser

# Parses the HTML
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
import pymongo

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

     # Set an empty dict for listings that we can save to Mongo
    mars_dict = {}

    # NASA Mars News
    # --------------------------
    #URL of page to be scrapes
    url = "https://redplanetscience.com/"
    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url)
    # Let it sleep for 1 second
    time.sleep(1)
    # Return all the HTML on our page
    html = browser.html
    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find('div', class_='list_text')
    news_title = article.find('div', class_='content_title').text
    news_p = article.find('div', class_='article_teaser_body').text

    # JPL Mars Space Images-Featured Image
    # ---------------------------------------------------------
    url = "https://spaceimages-mars.com"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    image = soup.find('img', class_='headerimage fade-in')["src"]
    featured_image_url = url + "/" + image

    # Mars Facts
    # --------------------------
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    html_table = df.to_html()

    # Mars Hemispheres
    # ----------------------------
    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    hemispheres = soup.find_all("div", class_="item")
    hemisphere_image_urls = []
    for i in hemispheres:
        title = i.find("h3").text
        hemispheres_img = i.find("a", class_="itemLink product-item")["href"]
        
        # Visit the link that contains the full image website 
        browser.visit(url + hemispheres_img)
        
        # HTML Object
        image_html = browser.html
        web_info = BeautifulSoup(image_html, "html.parser")
        
        # Create full image url
        img_url = url + web_info.find("img", class_="wide-image")["src"]
        
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    # Mars 
    mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "fact_table": html_table,
            "hemisphere_images": hemisphere_image_urls
        }
    print(mars_dict)
    return(mars_dict)
    browser.quit()
    





