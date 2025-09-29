import json

from dataaccess import UUID4


def success_conver_created(session_id: UUID4) -> dict:
    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"session_id": session_id}),
    }


def bad_request(message: str) -> dict:
    return {
        "statusCode": 400,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": message}),
    }


def ok(message: str) -> dict:
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"ai_response": message}),
    }


def internal_error(message: str) -> dict:
    return {
        "statusCode": 500,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": message}),
    }
