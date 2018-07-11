#Convert date and time to UTC_Published column
#Delete Date_Published and Time_Published 

import boto3

dynamodb = boto3.client('dynamodb')

def convUTC(item):
	#convert date_published and time_published to UTC timestamp
	both_pub = item['Date_Published'] + ' ' + item['Time_Published']
	dt = datetime.strptime(both_pub, '%Y-%m-%d %H:%M:%S')
	timestamp_item = (dt - datetime(1970, 1, 1)).total_seconds()
	return timestamp_item
	
	
#Insert item into DynamoDB Table but does not overwrite any items
self.dynamodb.update_item(
	TableName = 'CoindeskArticles',
	Key={'Title':{'S': item['title']}},
	UpdateExpression="SET UTC_Published=:tU",
	ExpressionAttributeValues={
		':tU': {"N": timestamp_item},
		}
)