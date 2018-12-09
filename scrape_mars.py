# Dependencies for web scraping
from bs4 import BeautifulSoup as bs
from splinter import Browser # Use splinter to automate browser actions
import requests

# Dependencies for data processing
import pandas as pd
import numpy as np


# Create a function that starts the splinter browser
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# Create a function that automates the web scraping
def scrape():
    browser = init_browser()

    # Empty dictionary (that will be placed as a collection in MongoDB)
    mars_current_data = {}


    ## NASA Mars website ##

    # Fetch the NASA Mars website for scraping
    url_NASA = "https://mars.nasa.gov/news"
    browser.visit(url_NASA)

    # Scrape for the news
    html_NASA = browser.html
    soup_NASA = bs(html_NASA, "html.parser")

    # News title and teaser
    news_title = soup_NASA.find("div", class_ = "content_title").text.strip()
    news_teaser = soup_NASA.find("div", class_ = "rollover_description_inner").text.strip()

    # Add to dictionary
    mars_current_data["latest_news_title"] = news_title
    mars_current_data["latest_news_teaser"] = news_teaser


    ## JPL featured image ##

    # JPL website
    url_JPL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_JPL)

    # Scrape for featured images
    html_JPL = browser.html
    soup_JPL = bs(html_JPL, "html.parser")

    # Get the URL of the featured image and its caption
    image = soup_JPL.find_all("a", class_ = "button fancybox")[0]
    image_url = image.get("data-fancybox-href")
    featured_image_url = "https://www.jpl.nasa.gov" + image_url

    image_caption = image.get("data-description")


    # Add to dictionary
    mars_current_data["featured_image"] = featured_image_url
    mars_current_data["featured_caption"] = image_caption


    ## Mars Weather ##

    # Fetch the Mars weather Twitter account
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    # Scrape for the latest twitter post on Mars weather
    html_twitter = browser.html
    soup_twitter = bs(html_twitter, "html.parser")

    # Find the latest Mars weather report 
    mars_weather = soup_twitter.find("p", class_ = "tweet-text").text

    # Add to dictionary
    mars_current_data["weather"] = mars_weather

    ## Mars facts ##

    # Fetch the Mars facts website
    url_facts = "https://space-facts.com/mars/"

    # Get the HTML table
    mars_facts = pd.read_html(url_facts) # list of dataframe objects
    len(mars_facts)

    # Convert the HTML table to a dataframe
    facts_df = mars_facts[0]
    facts_df.columns = ["Category", "Data"]

    # Convert the dataframe into HTML table
    # Resource: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_html.html
    facts_html = facts_df.to_html(index = False)

    # Add to dictionary
    mars_current_data["fun_facts"] = facts_html


    ## Images of Mars hemispheres ##

    # Extract photos of Mars hemispheres from the URL below
    url_hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Use splinter to visit the website
    browser.visit(url_hemi)

    # Create HTML object
    html_hemi = browser.html

    # Parse to derive a BeautifulSoup object
    soup_hemi = bs(html_hemi, "html.parser")

    # Retrieve the HTML elements with the link to each page containing
    desc_hemi = soup_hemi.find_all("div", class_ = "description")

    # Create a list of links
    partial_links = []
    for div in desc_hemi:
        for i in div.find_all("a"):
            partial_links.append(i.attrs["href"])

    comp_links = []        
    for x in partial_links:
        comp_links.append("https://astrogeology.usgs.gov/" + x)

    # Get and format the names of the hemispheres

    # remove the suffix "_enhanced"
    titles = [url.replace("_enhanced", "") for url in comp_links]

    # remove the base url
    titles = [title.replace("https://astrogeology.usgs.gov//search/map/Mars/Viking/", "") for title in titles]

    # remove underscores
    titles = [title.replace("_", " ") for title in titles]

    # capitalise the hemisphere names
    titles = [title.title() for title in titles]

    # Create a list of indices for scraping each hemisphere website using a loop
    index_links = list(np.arange(len(comp_links)))

    # Define a nested function that uses the index of each hemisphere website to get the image url
    def get_url(int):
        
        # Visit the url
        browser.visit(comp_links[int])
        
        # Scrape the contents
        html_link = browser.html
        soup = bs(html_link, "html.parser")
        
        # Extract the url of the full image
        img = soup.find_all("img", class_ = "wide-image")[0]
        inc_img_link = img.attrs["src"]
        comp_img_link = "https://astrogeology.usgs.gov" + inc_img_link
        
        return comp_img_link

    image_url = [get_url(idx) for idx in index_links]

    # Create a dataframe containing the names of the hemispheres and their respective urls
    hemi_df = pd.DataFrame({"title": titles, "image_url": image_url})

    # Mars hemispheres website
    hemisphere_images_urls = hemi_df.to_dict("records")

    # Add to dictionary
    mars_current_data["hemisphere_images"] = hemisphere_images_urls

    return mars_current_data