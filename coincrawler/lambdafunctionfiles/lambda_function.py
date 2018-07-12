import boto3
import json
import UTCConvertHelper
import querydb


#aws lambda update-function-code --function-name CoinDeskArticleGetter --zip-file fileb://lambda_function.zip



print('Loading function')
dynamo = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    ScanLimit = 100
	
    operations = {
        'GET': lambda dynamo, x, ScanLimit: querydb.get_query(dynamo, payload, ScanLimit),
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        return respond(None, operations[operation](dynamo, payload, ScanLimit))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
