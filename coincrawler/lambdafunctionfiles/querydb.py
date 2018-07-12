# dynamoDB Query Function Code

def get_query(dynamo, payload):
	
	validparams = ['author', 'date_pub', 'count', 'tablename', 'time_pub', 'title']
	
	#lowercase all keys 
	payload_lower = dict((k.lower(), v) for k,v in payload.items())
	
	# #Set None if the query parameter was not included
	# def mapping_params(paydict):
		# for param in validparams:
			# if param not in paydict:
				# paydict[param]=None
		# return paydict
		
	#function creates variables for dictionary unpacking into dynamodb scan function
	def scandict_input(tablename='CoindeskArticles', count=50, author=None, date_pub=None, time_pub=None, title=None):
		temp_dict = {'TableName': tablename, 'Limit':count}
		if author:
			temp_dict['FilterExpression'] = 'Author = :Au'
			temp_dict['ExpressionAttributeValues'] = {':Au':{'S': author.replace('-',' ')}}
			
		return temp_dict
		
			

	return dynamo.scan(**scandict_input(**payload_lower))
		
	

