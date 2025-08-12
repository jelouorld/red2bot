

resource "aws_lambda_function" "lambda" {
    filename      = "lambda.zip"
    function_name = "lambda"
    role          = aws_iam_role.lambda.arn
    handler       = "lambda.handler"
    runtime       = "nodejs12.x"
}
