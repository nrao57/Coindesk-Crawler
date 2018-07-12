# dynamoDB Query Function Code

def get_query(dynamo, payload, ScanLimit):
	validparams = ['Author', 'Date_Pub']
	
	if len(payload) == 1:
		return dynamo.scan(TableName='CoindeskArticles', Limit = ScanLimit)
	else:
		for param in payload:
			if param == 'Author':
				return dynamo.scan(
					TableName='CoindeskArticles',
					Limit = ScanLimit,
					FilterExpression='Author = :Au',
					ExpressionAttributeValues={':Au':{'S': payload['Author'].replace('-',' ')}}
					)