import boto3
import json
import router


ddb = boto3.resource("dynamodb")
table = ddb.Table("products")


@router.route("/products")
def products():
    pass


def process(event: dict):
    return {"event": event}
    # return {'event': table.scan().get('Items', [])}


def lambda_entrypoint(event: dict, context: dict):

    return router.dispatch(event)
