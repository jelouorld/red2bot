
data "archive_file" "lambda" {
    type        = "zip"
    source_dir  = var.srcdir
    output_path = var.srczip

}

resource "aws_lambda_function" "main" {
    function_name    = "main"
    filename         = data.archive_file.lambda.output_path
    source_code_hash = data.archive_file.lambda.output_base64sha256
    handler          = "main.main"
    runtime          = "python3.13"
    timeout          = 900
    role             = aws_iam_role.main_lambda_execution_role.arn
}

