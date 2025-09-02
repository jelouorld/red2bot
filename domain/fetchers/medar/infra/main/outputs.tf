

output "medar_fetcher_lambda_url" {
    value = aws_lambda_function_url.medar_fetcher_lambda_url.function_url
}