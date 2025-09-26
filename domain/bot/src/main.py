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
def chat(session_id: str):
    # execute all the langchain thing and return the response
    pass



def lambda_entrypoint(event: dict, context: dict):
    return router.dispatch(event)
