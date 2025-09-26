import boto3
import router
import typing as tp
import json

DDB = boto3.resource("dynamodb")
PRODUCTS_TABLE = DDB.Table("products")
CHATS_TABLE = DDB.Table("chats")


@router.route("/init", method="POST")
def init():
    # create a session_id
    # return a session_id
    return {'hello': 'world'}


@router.route("/chat/{session_id}", method="POST")
def chat(session_id: str, *, text=""):
    # text inyected by router, comes from event[body]
    # store thenew message
    # rebuild the context
    # the product data is in products
    # execute all thelancahin orchestration
    pass


@router.route("/event", method="GET")
def event(event: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
    return event


def lambda_entrypoint(event: dict, _):  # context unused
    # cli invocation
    if not event:
        return {"cli_invocation": True}
    return event
    return router.dispatch(event)
