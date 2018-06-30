# -*- coding: utf-8 -*-

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


