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
Data was obtained by web scraping using [Python](https://python.readthedocs.io/en/stable/contents.html)'s (version 3.6) [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library and the open-source tool [Splinter](https://splinter.readthedocs.io/en/latest/). Table 1 lists the startpoints for the web scraping and the information obtained from them.

Table 1. URLs used for web scraping news, weather information, and images about Mars
|Topic|URL|
|---|---|
|Latest News|https://mars.nasa.gov/news|
|Current Weather|https://twitter.com/marswxreport?lang=en|
|Mars Planetary Facts|https://space-facts.com/mars/|
|Featured Image|https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars|
|Images of Martian Hemispheres|https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars|

## Output