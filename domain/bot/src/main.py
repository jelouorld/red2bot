import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('products')

def main(event, context):
    try:
        response = table.scan(Limit=1)
        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps('No items found')
            }

        return {
            'statusCode': 200,
            'body': json.dumps(items[0])
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
