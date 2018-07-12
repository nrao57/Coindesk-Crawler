# dynamoDB Query Function Code

def get_query(dynamo, payload):
	validparams = ['Author', 'Date_Pub']
	for param in payload:
		if param == 'Author':
			return dynamo.scan(
				TableName='CoindeskArticles',
				Limit = 100,
				FilterExpression='Author = :Au',
				ExpressionAttributeValues={':Au':{'S': payload['Author'].replace('-',' ')}}
				)