
# <product_id, client_id, extension: rawJSON> 


resource "aws_dynamodb_table" "products" {
    name = "products"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "product_id"
    range_key = "client_id"

    attribute {
      name = "product_id"
      type = "S"
    }

    attribute {
      name = "client_id"
      type = "S"
    }
}

