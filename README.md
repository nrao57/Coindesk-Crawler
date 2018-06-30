
# CoinDesk Web Crawler using Scrapy library

## Introduction
[Scrapy](https://doc.scrapy.org/en/latest/index.html) is a powerful webscraping library for Python which allows for rapid development of web crawlers. It is a high level framework which provides many features otherwise absent in libraries like BeautifulSoup.

Today, we are going to create a web crawler to crawl the Bitcoin news site [Coindesk](https://www.coindesk.com/). Not only are we going to crawl the site, we are going to insert the link, title, date published, time published, and author of each article into a NoSQL database. And not just any database, but Amazon Web Service DyanmoDB.


![CoinDesk Logo](https://www.coindesk.com/wp-content/themes/coindesk2/images/footer-logo-square.png)
![AWS DyanmoDB Logo](https://upload.wikimedia.org/wikipedia/commons/f/fd/DynamoDB.png)

## To Create a New Scrapy Project

1. Download Scrapy package
2. Type `scrapy startproject coincrawler`

## Directory and Files 
When the `scrapy startproject` command is executed, scrapy creates the following directory structure

```
tutorial/
    scrapy.cfg            # deploy configuration file

    coincrawler/  # project's Python module, your code will be here
        
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # directory where with your spiders
            __init__.py
```

### What are the Other Files?
For our spider, nothing changes in settings
pipelines.py contains all the processing of one page/item
Middlewares dont change
init does not change

## Scrapy Interpreter
In order to scrape and gather data from any website you need to understand the underlying html and css format. Luckily, Scrapy has a built-in shell tool to help parse and explore the underlying structure of the web page we are interested in. [Scrapy's official documentation](https://doc.scrapy.org/en/latest/topics/shell.html#topics-shell) has a great tutorial on using the shell tool to extract data.

## Creating Our Spider


```python
import scrapy

class CoinDeskCrawler(scrapy.Spider):
    name = "CoinDesk"
    max_pagenum = 924 #924 
    mainpath = 'https://www.coindesk.com/page/'
    start_urls = [mainpath + '{}/'.format(i) for i in range(1,max_pagenum+1)]
    
    def parse(self, response):
        # follow links to article pages
        for href in response.css('a.fade::attr(href)'):
            yield response.follow(href, self.parse_article)
            
    def parse_article(self, response):
        #Get name of url you are opening
        page = response.url.split("/")[-2]
        filename = 'coindesk-%s.txt' % page
        yield {
            'link': response.url,
            'title': str(response.css('title::text').extract_first()),
            'date_published': str(response.xpath("//meta[@property='article:published_time']/@content")[1].extract()).split("T")[0],
            'time_published': str(response.xpath("//meta[@property='article:published_time']/@content")[1].extract()).split("T")[1],
            'author': str(response.css('div.article-top-author-block-right-upper').css('a::text').extract_first()),
            }
    

```

## Creating an Item Pipeline

Item pipelines are contained in the pipelines.py file and processes items after they have been scraped by your spider. Item Pipelines process these scraped items through several components that are executed sequentially. 

These processes include:
 `open_spider()`
 `close_spider()`
 `process_item()`

Common uses for Item pipelines include:

* cleansing HTML data
* validating scraped data (checking that the items contain certain fields)
* checking for duplicates (and dropping them)
* storing the scraped item in a database

Also, Don't forget to add your pipeline to the ITEM_PIPELINES setting!!!

See: [Scrapy Official Documentation](https://doc.scrapy.org/en/latest/topics/item-pipeline.html)


```python
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import boto3
from scrapy.exceptions import DropItem


class CoincrawlerPipeline(object):
    def open_spider(self, spider):
        ## AWS DynamoDB Connection
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')
        # Get the table
        self.table = dynamodb.Table('CoinDeskArticles')
                
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item:
            with self.table.batch_writer() as batch:
                batch.put_item(
                    Item={
                        'Title': item['title'],
                        'Date': item['date_published'],
                        'Time': item['time_published'],
                        'Author': item['author'],
                        'Link': item['link'],
                        }
                )
            return item
        else:
            raise DropItem()
```

The `open_spider` method opens the DyanmoDB resource in our AWS account and saves the DynamoDB table of our choosing (in this case I have a DynamoDB table called "CoinDeskArticles") as an instance variable. Note that this method will be called first when the spider begins crawling 

The `process_item` method where all the processing magic happends. The `item` parameter is the dictionary yielded by the Coindesk Spider. The `process_item` method takes each dictionary and inserts the item into the DyanamoDB table with the fields "Title", "Date", "Time", "Author", amd "Link".

## Running the Spider
To run our spider on the Coindesk website, all you have to do is run the command `scrapy crawl coincrawler`

What just happend?

Scrapy schedules the scrapy.Request objects returned by the start_requests method of the Spider. The start_requests method uses the start_urls class attribute to create the intitial requests for your spider. Upon receiving a response for each one, it instantiates Response objects and calls the callback method associated with the request (in this case, the parse method) passing the response as argument.
