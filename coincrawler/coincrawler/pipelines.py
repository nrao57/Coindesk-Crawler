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
			#convert date_published and time_published to UTC timestamp
			both_pub = item['date_published'] + ' ' + item['time_published']
			dt = datetime.strptime(both_pub, '%Y-%m-%d %H:%M:%S')
			timestamp_item = (dt - datetime(1970, 1, 1)).total_seconds()
			#Insert item into DynamoDB Table but does not overwrite any items
			self.dynamodb.update_item(
				TableName = 'CoindeskArticles',
				Key={'Author':{'S': item['author']}},
				UpdateExpression="SET UTC_Published=:tU, Title=:tI, Link=:Li",
				ExpressionAttributeValues={
					':tU': {"N": timestamp_item},
					':tI':{"S": item['title']},
					':Li':{"S": item['link']}
					}
			)
			return item
		else:
			raise DropItem()


