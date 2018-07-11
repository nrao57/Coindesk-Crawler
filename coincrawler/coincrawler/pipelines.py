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
		self.dynamodb = boto3.client('dynamodb')

				
    def close_spider(self, spider):
		# publish a message to sns alert when the spider
		# is finished running
		client = boto3.client('sns')
		client.publish(
			TopicArn='arn:aws:sns:us-east-1:547950090894:WebCrawlerAlerts',
			Message='Finally! The Coin Desk Web Crawler has finished',
			Subject='Coin Desk Web Crawler has finished'
		)
		

    def process_item(self, item, spider):
		if item:
			#Insert item into DynamoDB Table but does not overwrite any items
			self.dynamodb.update_item(
				TableName = 'CoindeskArticles',
				Key={'Title':{'S': item['title']}},
				UpdateExpression="SET Date_Published=:dP, Time_Published=:tP, Author=:au, Link=:Li",
				ExpressionAttributeValues={
					':dP': {"S": item['date_published']},
					':tP':{"S": item['time_published']},
					':au':{"S": item['author']},
					':Li':{"S": item['link']}
					}
			)
			return item
		else:
			raise DropItem()


