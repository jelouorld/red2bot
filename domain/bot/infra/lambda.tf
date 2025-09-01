
data "archive_file" "lambda" {
    type        = "zip"
    source_dir  = var.srcdir
    output_path = var.srczip

}

resource "aws_lambda_function" "main" {
    function_name    = "red2bot"
    filename         = data.archive_file.lambda.output_path
    source_code_hash = data.archive_file.lambda.output_base64sha256
    handler          = "main.lambda_entrypoint"
    runtime          = "python3.13"
    timeout          = 900
    role             = aws_iam_role.main_lambda_execution_role.arn
}


resource "aws_lambda_function_url" "red2bot_url" {
    function_name      = aws_lambda_function.main.function_name
    authorization_type = "NONE"
}
