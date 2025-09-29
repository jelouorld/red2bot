import json

from dataaccess import UUID4


def success_created(session_id: UUID4) -> dict:
    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"session_id": session_id}),
    }


def error(message: str) -> dict:
    return {
        "statusCode": 500,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": message}),
    }
