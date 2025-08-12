
data "aws_iam_policy_document" "lambda_trust_policy" {
    statement {
        actions = ["sts:AssumeRole"]
        effect = "Allow"
        principals {
            type        = "Service"
            identifiers = ["lambda.amazonaws.com"]
        }
    }
}


data "aws_iam_policy_document" "dynamodb_rw_policy" {
    statement {
        actions = [
            "dynamodb:BatchGetItem",
            "dynamodb:GetItem",
            "dynamodb:Query",
            "dynamodb:Scan",
            "dynamodb:BatchWriteItem",
            "dynamodb:PutItem",
            "dynamodb:UpdateItem",
        ]
        effect = "Allow"
        resources = [
            aws_dynamodb_table.chats.arn,
            aws_dynamodb_table.products.arn,
        ]
    }
} 



resource "aws_iam_role" "main_lambda_execution_role" {
    name = "main_lambda_execution_role"
    assume_role_policy = data.aws_iam_policy_document.lambda_trust_policy.json
}

# Attachemnt: Basic policy; read/write cloudwatch logs
resource "aws_iam_role_policy_attachment" "basic_policy_attachment" {
    role = aws_iam_role.main_lambda_execution_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


 # Add an inline policy for rw chats and products 

resource "aws_iam_role_policy" "dynamodb_rw_policy" {
    name = "dynamodb_rw_policy"
    role = aws_iam_role.main_lambda_execution_role.id
    policy = data.aws_iam_policy_document.dynamodb_rw_policy.json
}


