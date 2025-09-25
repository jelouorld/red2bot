
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


data "aws_iam_policy_document" "dynamodb_products_write_policy" {
    statement {
        actions = [
            "dynamodb:BatchWriteItem",
            "dynamodb:PutItem",
            "dynamodb:UpdateItem",
        ]
        effect = "Allow"
        resources = [
            data.aws_dynamodb_table.products.arn,
        ]
        
    }
} 

data aws_iam_policy_document "kms_access" {
    statement {
        actions = ["kms:Decrypt",]
        effect = "Allow"
        resources = ["*"]
    }
}

resource "aws_iam_role" "medar_fetcher_lambda_execution_role" {
    name = "medar_fetcher_lambda_execution_role"
    assume_role_policy = data.aws_iam_policy_document.lambda_trust_policy.json
}

# Attachemnt: Basic policy; read/write cloudwatch logs
resource "aws_iam_role_policy_attachment" "basic_policy_attachment" {
    role = aws_iam_role.medar_fetcher_lambda_execution_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


# Add an inline policy for rw chats and products 
resource "aws_iam_role_policy" "dynamodb_rw_policy" {
    name = "medar_fetcher_dynamodb_rw_policy"
    role = aws_iam_role.medar_fetcher_lambda_execution_role.id
    policy = data.aws_iam_policy_document.dynamodb_products_write_policy.json
}

resource "aws_iam_role_policy" "kms_access_inline_policy" {
    name = "medar_fetcher_kms_access_policy"
    role = aws_iam_role.medar_fetcher_lambda_execution_role.id
    policy = data.aws_iam_policy_document.kms_access.json
}


