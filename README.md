# Mission to Mars
![alt text](https://www.jpl.nasa.gov/images/mars/20170622/PIA01466-16.jpg)
*Panorama photo taken by the Mars Pathfinder in 1997.*

## Introduction
[Mars](https://physicstoday.scitation.org/do/10.1063/PT.5.3040/full/) has long been the subject of science fiction; it is seen as a place that humans could settle in when they need safe refuge from an Earth-wide catastrophe. A project, called [Mars One](http://www.digitaljournal.com/article/325858), intends to create habitable settlements for humans by 2023. But before humans could take the [150- to 300-day journey](https://www.universetoday.com/14841/how-long-does-it-take-to-get-to-mars/) (depending on the speed of the spacecraft and the relative positions of the Earth and Mars), scientists took to the task to discover the planet's [potential for human habitation](https://mars.nasa.gov/programmissions/overview/). The National Aeronautics and Space Administration ([NASA](https://www.nasa.gov/about/index.html)) has launched several missions in [three stages](https://marsmobile.jpl.nasa.gov/programmissions/missions/): flybys; orbits; and landings and surface explorations. The most recent mission has seen the [successful soft landing](https://mars.nasa.gov/news/8392/nasa-insight-lander-arrives-on-martian-surface/) of the Interior Exploration using Seismic Investigations, Geodesy and Heat Transport (InSight) lander on Mars on November 26, 2018. This further boosts NASA's capacity to collect and to transmit data in real-time back to Earth. In fact, InSight allowed Earthlings to hear, for the first time, [Martian winds](https://mars.nasa.gov/news/8397/nasa-insight-lander-hears-martian-winds/).

Thanks to the sensors that are now in place on Mars, it is now possible to collect information. The web app "On the Red Planet" features the latest news from NASA's [Mars Exploration Program](https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest) and the most recent weather update from [Curiosity rover](https://twitter.com/marswxreport?lang=en). The app also shows featured images from the [Jet Propulsion Laboratory](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) of the California Institute of Technology and photos of the four hemispheres of Mars referred to based on their unique features:
1. [__Cerberus__](https://en.wikipedia.org/wiki/Cerberus_(Martian_albedo_feature)), a large dark spot believed to be composed of lava
2. [__Schiaparelli__](https://en.wikipedia.org/wiki/Schiaparelli_(Martian_crater)#cite_note-Gazetteer-Schiaparelli-1), an impact crater near the Martian equator
3. [__Syrtis Major__](https://en.wikipedia.org/wiki/Syrtis_Major_Planum), another dark spot, believed to be a shield volcano
4. [__Valles Marineris__](https://en.wikipedia.org/wiki/Valles_Marineris), a series of canyons which could be a tectonic crack on the planet's surface 

## Method
### Web scraping
Data was obtained by web scraping using [Python](https://python.readthedocs.io/en/stable/contents.html)'s (version 3.6) [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library and the open-source tool [Splinter](https://splinter.readthedocs.io/en/latest/). [Pandas](https://pandas.pydata.org/pandas-docs/stable/) and [Numpy](https://docs.scipy.org/doc/numpy-1.15.0/) were used to process the data obtained from scraping the websites in Table 1. 

```python
# Dependencies for web scraping
from bs4 import BeautifulSoup as bs
from splinter import Browser # Use splinter to automate browser actions
import requests

# Dependencies for data processing
import pandas as pd
import numpy as np
```

Table 1. URLs used for web scraping news, weather information, and images about Mars

|Topic|URL|variable in `scrape_mars.py`|
|---|---|---|
|Latest News|https://mars.nasa.gov/news|url_NASA|
|Current Weather|https://twitter.com/marswxreport?lang=en|url_twitter
|Mars Planetary Facts|https://space-facts.com/mars/|url_facts|
|Featured Image|https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars|url_JPL|
|Images of Martian Hemispheres|https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars|url_hemi|

The codes were originally written in [mission_to_mars.ipynb](https://github.com/rochiecuevas/Mission_Mars/blob/master/mission_to_mars.ipynb) and was converted to the [scrape_mars.py](https://github.com/rochiecuevas/Mission_Mars/blob/master/scrape_mars.py) python script using the following [code](https://nbconvert.readthedocs.io/en/latest/usage.html) in the command line:

```python
jupyter nbconvert --to python mission_to_mars.ipynb
```

__Note:__ *Because the python script was used in creating the Flask application, this script is featured below. The Jupyter notebook was used for testing the codes prior to developing the web application.*

Before conducting web scraping, the function `init_browser()` was defined, which could start the splinter browser. The open-source tool [chromedriver](http://chromedriver.chromium.org/) needed to be downloaded to make sure that the code below works. The path of the chromedriver also needed to be determined (using the `!which chromedriver` code in the Jupyter notebook). 

```python
# Create a function that starts the splinter browser
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
```

Next, the web scraping script `scrape` was defined.

```python
# Create a function that automates the web scraping
def scrape():
    browser = init_browser()
```

An empty dictionary `mars_current_data` was created. This dictionary would contain the outputs of web scraping originating from the URLs in Table 1.

The __first__ step in scraping was creating a Beautiful Soup object, which basically is the website content in a nested data structure. For example, for the latest news from NASA followed Table 2. These steps were conducted also for the other URL variables in Table 1.

Table 2. Workflow for creating the Beautiful Soup object for latest news stored in `url_NASA`.

|Step No| Description|Code|
|---|---|---|
|1|Access the URL|`browser.visit(url_NASA)`|
|2|Verify content of the URL|`html_NASA = browser.html`|
|3|Create a soup object|`soup_NASA = bs(html_NASA, "html.parser")`|

To help track the variables, see Table 3.

Table 3. Traceability from URL variable to Beautiful Soup object for text data.

|Content|URL variable|html variable|bs object|
|---|---|---|---|
|latest news|url_NASA|html_NASA|soup_NASA|
|featured image|url_JPL|html_JPL|soup_JPL|
|current weather|url_twitter|html_twitter|soup_twitter|
|Martian hemispheres|url_hemi|html_hemi|soup_hemi|

The __second__ step in scraping was finding the HTML tags that contained the relevant data and isolating the conntent. Because each website has a unique design, finding this step was customised for each soup object. __NB:__ *The codes are indented because they are inside the function `scrape()`*.

```python
# News title and teaser
    news_title = soup_NASA.find("div", class_ = "content_title").text.strip()
    news_teaser = soup_NASA.find("div", class_ = "rollover_description_inner").text.strip()

# Get the URL of the featured image and its caption
    image = soup_JPL.find_all("a", class_ = "button fancybox")[0]
    image_url = image.get("data-fancybox-href")
    featured_image_url = "https://www.jpl.nasa.gov" + image_url
    image_caption = image.get("data-description")

# Find the latest Mars weather report 
    mars_weather = soup_twitter.find("p", class_ = "tweet-text").text
```

Getting the planetary data required a different approach because the data was in a HTML table. Hence, [`pd.read_html()`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_html.html) was used to extract this HTML table into a list of dataframe objects.

```python
# Get the HTML table
    mars_facts = pd.read_html(url_facts) # list of dataframe objects
    len(mars_facts)

# Convert the HTML table to a dataframe
    facts_df = mars_facts[0]
    facts_df.columns = ["Category", "Data"]
```

The data was then converted to a HTML table.

```python
# Convert the dataframe into HTML table
# Resource: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_html.html
    facts_html = facts_df.to_html(index = False)
```

The hemisphere images were located in four separate webpages with links in `url_hemi`. Hence, the divs for these links were obtained as follows:

```python
# Retrieve the HTML elements with the link to each page containing
    desc_hemi = soup_hemi.find_all("div", class_ = "description")
```

The webpage URLs were inside the <a></a> children of the <div class = "description"> HTML tag. A for-loop was used to extract the URLs:

```python
# Create a list of links
    partial_links = []
    for div in desc_hemi:
        for i in div.find_all("a"):
            partial_links.append(i.attrs["href"])

    comp_links = []        
    for x in partial_links:
        comp_links.append("https://astrogeology.usgs.gov/" + x)
```

The names of each hemisphere, were put in a list called `titles` and cleaned.

```python
# remove the suffix "_enhanced"
    titles = [url.replace("_enhanced", "") for url in comp_links]

# remove the base url
    titles = [title.replace("https://astrogeology.usgs.gov//search/map/Mars/Viking/", "") for title in titles]

# remove underscores
    titles = [title.replace("_", " ") for title in titles]

# capitalise the hemisphere names
    titles = [title.title() for title in titles]
```

To recap, the name and the URL of the webpage of each hemisphere were appended to the `titles` and `comp_links` lists, respectively. The URL of each hemisphere image was obtained using the function `get_url()` based on the indices of each webpage URL in `comp_links`. This function was nested inside `scrape()`.

```python
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
```

The two lists, `titles` and `image_url`, were placed in a dataframe

```python
hemi_df = pd.DataFrame({"title": titles, "image_url": image_url})
```

and then converted into a dictionary.

```python
hemisphere_images_urls = hemi_df.to_dict("records")
```

__Note:__ *[`df.to_dict("records")`](https://stackoverflow.com/a/37897753) allows one to use each column header as a key and each row value as a value in a list of dictionaries (each dictionary corresponds to each row in the dataframe).*

The __third__ step in this workflow was adding the final outputs of each web scrape to the dictionary `mars_current_data`. This was done right after each final output was generated.

```python
    mars_current_data["latest_news_title"] = news_title
    mars_current_data["latest_news_teaser"] = news_teaser
    mars_current_data["featured_image"] = featured_image_url
    mars_current_data["featured_caption"] = image_caption
    mars_current_data["weather"] = mars_weather
    mars_current_data["fun_facts"] = facts_html
    mars_current_data["hemisphere_images"] = hemisphere_images_urls
```

Hence, the function `scrape` returned the dictionary.

```python
    return mars_current_data
```

### Loading Mars data into MongoDB

## Output