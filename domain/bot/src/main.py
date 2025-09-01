
import json

import boto3


ddb=boto3.client('dynamodb')



def lambda_handler(event:dict, context:dict):

    table = ddb.TableName('test')

    
    return {

        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


