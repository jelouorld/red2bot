
import boto3

DDB = boto3.resource("dynamodb")
PRODUCTS_TABLE = DDB.Table("products")
CHATS_TABLE = DDB.Table("chats")
