resource "aws_dynamodb_table" "chats" {
  name           = "chats"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "session_id"
  range_key      = "timestamp"

  attribute {
    name = "session_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  tags = {
    Environment = "dev"
    Service     = "red2bot"
  }
}
