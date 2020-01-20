### Databases
#### Problem set 2: Web Scraping
- Site: IMDB - scraping current showing times at link: https://www.imdb.com/showtimes/20XX-XX-XX 

##### Description
- This web scraper crawls movie showtime information for a four-day period (including the initial specified date) from the IMDB website. The initial date is specified in ``imdb_crawler/imdb_crawler/spiders/showtimes.py`` file, indicated by year-month-day format (XXXX-XX-XX)
- The scraped data is then stored in a MongoDB (NoSQL), with the database name 'imdb' and collection name 'showtimes.'

##### How to run
-- ``cd imdb_crawler`` (root directory)
-- ``scrapy crawl imdb_crawler``

##### Check mongo database
-- ``use imdb``
-- ``db.showtimes.find( {showday:"2019-10-29"} )``