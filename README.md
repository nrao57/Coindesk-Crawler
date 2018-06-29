
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

### What are the Other Files?
nothing changes in settings
pipelines.py contains all the processing of one page/item
Middlewares dont change
init does not change

## Scrapy Interpreter

## DyanmoDB

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
