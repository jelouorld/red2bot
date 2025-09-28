import boto3
import router
import typing as tp
import json
import uuid


DDB = boto3.resource("dynamodb")
PRODUCTS_TABLE = DDB.Table("products")
CHATS_TABLE = DDB.Table("chats")


@router.route("/init", method="POST")
def init():
    # create a session_id
    # return a session_id
    try:
        session_id = str(uuid.uuid4())
        CHATS_TABLE.put_item(Item={"session_id": session_id})
        return {
            "statusCode": 201, 
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({'session_id': session_id})
        }
    except Exception as e:
        return {
            "statusCode": 500, 
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({'error': str(e)})
        }
    
    

@router.route("/chat/{session_id}", method="POST")
def chat(session_id: str, *, text=""):
    # text inyected by router, comes from event[body]
    # store thenew message
    # rebuild the context
    # the product data is in products
    # execute all thelancahin orchestration
    return {"session_id": session_id, "text": text}


@router.route("/event", method="GET")
def event(event: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
    return event


def lambda_entrypoint(event: dict, _):  # context unused
    # cli invocation
    if not event:
        return {"cli_invocation": True}

    return router.dispatch(event)