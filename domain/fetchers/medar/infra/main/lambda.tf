
data "archive_file" "lambda" {
    type        = "zip"
    source_dir  = var.srcdir
    output_path = var.srczip
}

resource "aws_lambda_function" "medar_fetcher" {
    function_name    = "medar_fetcher"
    filename         = data.archive_file.lambda.output_path
    source_code_hash = data.archive_file.lambda.output_base64sha256
    handler          = "main.lambda_entrypoint"
    runtime          = "python3.13"
    timeout          = 900
    role             = aws_iam_role.medar_fetcher_lambda_execution_role.arn

    environment {
        variables = {
            FETCHER_ENV="CLI_INVOKE"
        }
    }
}


resource "aws_lambda_function_url" "medar_fetcher_lambda_url" {
    function_name      = aws_lambda_function.medar_fetcher.function_name
    authorization_type = "NONE"
}


