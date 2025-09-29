import boto3

ddb = boto3.client("dynamodb")
lambda_service = boto3.client("lambda")


def test_main_lambda_function():
    lambda_service = boto3.client("lambda")
    response = lambda_service.list_functions()

    functions = response.get("Functions", [])

    assert len(functions) > 0

    assert any("red2bot" in f["FunctionName"] for f in functions)


def test_dynamodb_tables():
    tables = ddb.list_tables()["TableNames"]

    assert "products" in tables
    assert "chats" in tables
