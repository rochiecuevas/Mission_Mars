# Mission to Mars
![alt text](https://www.jpl.nasa.gov/images/mars/20170622/PIA01466-16.jpg)
*Panorama photo taken by the Mars Pathfinder in 1997.*

## Introduction
[Mars](https://physicstoday.scitation.org/do/10.1063/PT.5.3040/full/) has long been the subject of science fiction; it is seen as a place that humans could settle in when they need safe refuge from an Earth-wide catastrophe. A project, called [Mars One](http://www.digitaljournal.com/article/325858), intends to create habitable settlements for humans by 2023. But before humans could take the [150- to 300-day journey](https://www.universetoday.com/14841/how-long-does-it-take-to-get-to-mars/) (depending on the speed of the spacecraft and the relative positions of the Earth and Mars), scientists took to the task to discover the planet's [potential for human habitation](https://mars.nasa.gov/programmissions/overview/). The National Aeronautics and Space Administration ([NASA](https://www.nasa.gov/about/index.html)) has launched several missions in [three stages](https://marsmobile.jpl.nasa.gov/programmissions/missions/): flybys; orbits; and landings and surface explorations. The most recent mission has seen the [successful soft landing](https://mars.nasa.gov/news/8392/nasa-insight-lander-arrives-on-martian-surface/) of the Interior Exploration using Seismic Investigations, Geodesy and Heat Transport (InSight) lander on Mars on November 26, 2018. This further boosts NASA's capacity to collect and to transmit data in real-time back to Earth. In fact, InSight allowed Earthlings to hear, for the first time, [Martian winds](https://mars.nasa.gov/news/8397/nasa-insight-lander-hears-martian-winds/).

Thanks to the sensors that are now in place on Mars, it is now possible to collect information. The web app "On the Red Planet" features the latest news from NASA's [Mars Exploration Program](https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest) and the most recent weather update from the [Curiosity rover](https://twitter.com/marswxreport?lang=en). The app also shows featured images from the [Jet Propulsion Laboratory](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) of the California Institute of Technology and photos of the four hemispheres of Mars referred to based on their unique features:
1. [__Cerberus__](https://en.wikipedia.org/wiki/Cerberus_(Martian_albedo_feature)), a large dark spot believed to be composed of lava
2. [__Schiaparelli__](https://en.wikipedia.org/wiki/Schiaparelli_(Martian_crater)#cite_note-Gazetteer-Schiaparelli-1), an impact crater near the Martian equator
3. [__Syrtis Major__](https://en.wikipedia.org/wiki/Syrtis_Major_Planum), another dark spot, believed to be a shield volcano
4. [__Valles Marineris__](https://en.wikipedia.org/wiki/Valles_Marineris), a series of canyons which could be a tectonic crack on the planet's surface 

## Method
### Extracting data by web scraping and data transformation
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

The codes were originally written in [mission_to_mars.ipynb](https://github.com/rochiecuevas/Mission_Mars/blob/master/mission_to_mars.ipynb) and were converted to the [scrape_mars.py](https://github.com/rochiecuevas/Mission_Mars/blob/master/scrape_mars.py) python script using the following [code](https://nbconvert.readthedocs.io/en/latest/usage.html) in the command line:

```html
jupyter nbconvert --to python mission_to_mars.ipynb
```

__Note:__ *Because the python script was used in creating the Flask application, this script is featured below. The Jupyter notebook was used for testing the codes prior to developing the web application and is not detailed in the README.*

Before conducting web scraping, the function `init_browser()` was defined, which could start the splinter browser. The open-source tool [chromedriver](http://chromedriver.chromium.org/) needed to be downloaded to make sure that the code below works. The path of the chromedriver also needed to be determined (using the `!which chromedriver` code in the Jupyter notebook). 

```python
# Create a function that starts the splinter browser
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
```

Next, the web scraping function `scrape` was defined.

```python
# Create a function that automates the web scraping
def scrape():
    browser = init_browser()

    mars_current_data = {}
```

An empty dictionary `mars_current_data` was created. This dictionary would contain the outputs of web scraping originating from the URLs in Table 1.

The __first__ step in scraping was creating a Beautiful Soup object, which basically is the website content in a nested data structure. For example, web scraping for the latest news from NASA followed Table 2. These steps were conducted also for the other URL variables in Table 1.

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

The __second__ step in scraping was finding the HTML tags that contained the relevant data and isolating the content. Because each website has a unique design, this step was customised for each soup object. __NB:__ *The codes are indented because they are inside the function `scrape()`*.

```python
# News title and teaser
    news_title = soup_NASA.find("div", class_ = "content_title").text.strip()
    news_teaser = soup_NASA.find("div", class_ = "rollover_description_inner").text.strip()

# URL of the featured image and its caption
    image = soup_JPL.find_all("a", class_ = "button fancybox")[0]
    image_url = image.get("data-fancybox-href")
    featured_image_url = "https://www.jpl.nasa.gov" + image_url
    image_caption = image.get("data-description")

# Latest Mars weather report 
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

The data was then converted to a new HTML table.

```python
# Convert the dataframe into HTML table
# Resource: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_html.html
    facts_html = facts_df.to_html(index = False)
```

The hemisphere images were located in four separate webpages with links in `url_hemi`. The webpage URLs were inside the `<a></a>` children of the `<div class = "description">` HTML tag. To get to the URLs, the description div classes were isolated:

```python
# Retrieve the HTML elements with the link to each page containing
    desc_hemi = soup_hemi.find_all("div", class_ = "description")
```

 A for-loop was then used to extract the URLs:

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

The name of each hemisphere was put in a list called `titles` and then cleaned.

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

To recap, the name and the URL of the webpage of each hemisphere were appended to the `titles` and the `comp_links` lists, respectively. The URL of each hemisphere image was obtained using the function `get_url()` based on the index of each webpage URL in `comp_links`. This function was nested inside `scrape()`.

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

Hence, the function `scrape` returned the now populated dictionary.

```python
    return mars_current_data
```

### Building the `index.html` page
A `templates` folder was created to store the [`index.html`](https://github.com/rochiecuevas/Mission_Mars/blob/master/templates/index.html) file. This would allow [`app.py`](https://github.com/rochiecuevas/Mission_Mars/blob/master/app.py) to extract from the MongoDB database directly and load onto the webpage. The `index.html` used Bootstrap CSS for formatting and layouting. 

A button on the `<div class = "jumbotron">` that acted like a link to `app.py` was added. Each time this button was clicked, the most updated information about Mars from the NASA mission was placed in `index.html`.

```html
<a class = "btn btn-info btn-lg" href = "/scrape">Live: From Mars!</a>
```


The information from the list `info` was placed into the html page. For example, the latest news was rendered as follows:

```html
<h3>{{ list.news_title }}</h3> <!-- news title -->
<p>{{ list.news_teaser }}</p> <!-- news teaser -->
```

The HTML table of Mars planetary data was rendered onto `index.html` using this code:

```html
{{ list.fun_facts | safe}} <!-- "|safe }}" allows the HTML table to be rendered directly -->
```

The URL of the featured image was inserted as a string in the image HTML tag.

```html
<img src = "{{ list.featured_image }}" alt = "featured image" width = 100%/>
```

To render each hemisphere image, the list of dictionaries containing the hemisphere URLs (in the BSON document created by `app.py`) was subjected to a for loop.

```html
{% for pic in list.hemisphere_images[2:4] %}
<img src = "{{ pic['image_url'] }}" alt = "hemisphere_pic" width = 100% />
<div class = "caption"><i>{{ pic['title'] }}</i></div>
{% endfor %}
```

In the code above, `{{ pic['image_url'] }}` referred to the value while `{{ pic['title'] }}` referred to the field for each dictionary in the list.

### Loading Mars data into MongoDB
The data stored in `mars_current_data` was loaded into MongoDB using the [Flask](http://flask.pocoo.org/docs/1.0/) app `app.py`. This was initiated by loading Flask, [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/), and `scrape_mars.py`.

```python
# Dependencies for database CRUD
from flask_pymongo import PyMongo # Use flask_pymongo to allow running MongoDB in Python
import scrape_mars

# Dependencies for rendering the information to HTML
from flask import Flask, render_template, redirect
```

The app was initialised and configured for MongoDB.

```python
# Create an instance for the Flask app
app = Flask(__name__)

# Connect to a MongoDB database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
```

Two app routes were created. The first one rendered to the `index.html` file while the second one directed to `/scrape`, which then redirected to the `index.html`. The first app route had a function called `index` that extracted the first BSON document in the database and placed it in a list called `info` in the database.

```python
@app.route('/')
def index():
    # Store the collection in a list
    info = mongo.db.mars_current_data.find_one()

    # Render the template with the information in it
    return render_template("index.html", list = info)
```

The second app route defined a function called `scraper` which called the `scrape()` function in `scrape_mars.py`. The `mars_current_dictionary` returned by `scrape()` was loaded as a BSON document into the database. 

```python
@app.route('/scrape')
def scraper():
    info = mongo.db.mars_current_data
    info_data = scrape_mars.scrape()
    info.update({}, info_data, upsert = True)
    return redirect("/", code = 302)
```

Before running `app.py`, MongoDB was initialised in the command line.

```html
$ mongod
```

## Output
[`app.py`](https://github.com/rochiecuevas/Mission_Mars/blob/master/app.py) was run in the development environment from the command line.

```html
$ export FLASK_DEBUG=1
$ export FLASK_ENV=development
$ export FLASK_APP=app.py
$ flask run
```

Opening the route `http://127.0.0.1:5000/` led automatically to loading `index.html` on the browser. Clicking the `Live: From Mars!` button would rerun `app.py` and show the latest data.