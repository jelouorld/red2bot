import boto3
import json
import router


ddb = boto3.resource("dynamodb")
table = ddb.Table("products")


@router.route("/init", method="POST")
def init():
    # create a session_id 
    # return a session_id 
    pass


@router.route("/chat/{session_id}", method="POST")
def chat(session_id: str, *, text=""):
    # text inyected by router, comes from event[body]
    # store thenew message ç
    # rebuild the context 
    # the product data is in products 
    # execute all thelancahin orchestration
    
    pass



def lambda_entrypoint(event: dict, context: dict):
    return router.dispatch(event)
