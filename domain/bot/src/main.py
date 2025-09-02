
import boto3

import json

import decimal as d 


def decimal_decode(obj: d.Decimal):
    if isinstance(obj, d.Decimal):
        return float(obj)
    raise TypeError


ddb=boto3.resource('dynamodb')
table=ddb.Table('products')


def lambda_entrypoint(event:dict, context:dict):
    return {
        'event': table.scan().get('Items', [])
    }


# if __name__ == '__main__':
#     print(lambda_entrypoint(None, None))





