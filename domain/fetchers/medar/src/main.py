import boto3

ddb=boto3.client("dynamodb")

# envs:
# local -> local
# cloud -> manual invoke 
# cloud -> scheduled <(special case) manual 


def lambda_entrypoint(event, context):
    return {
        "statusCode": 200,
        "body": "Hello from Lambda!"
    }

