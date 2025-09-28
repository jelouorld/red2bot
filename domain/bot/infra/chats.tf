
resource "aws_dynamodb_table" "chats" {
    name = "chats"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "session_id"

    attribute {
      name = "session_id"
      type = "S"
    }

    # messages array at runtime 
    # array of objects: ref: base/schemas/v1/chats.tf
    # schema: <role: {assistant, user}, content: string, timestamp: timestamp>

}


