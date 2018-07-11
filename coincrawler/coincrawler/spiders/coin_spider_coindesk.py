#CoinDeskCrawler using Scrapy library
import scrapy

class CoinDeskCrawler(scrapy.Spider):
	name = "CoindeskCrawler"

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
	
			



