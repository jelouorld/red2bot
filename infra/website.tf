
# S3 for website hosting
resource "aws_s3_bucket" "website" {
    bucket = "red2bot-website"

    tags =  {
        Environment = "dev"
    }
    
}


resource "aws_s3_bucket_public_access_block" "website_buckewebswebit_public_access_block" {
    bucket = aws_s3_bucket.website.id

    block_public_acls = false
    block_public_policy = false
    ignore_public_acls = true
    restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "website_bucket_policy" {
    bucket = aws_s3_bucket.website.id

    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::${aws_s3_bucket.website.id}/*"
            ]
        }
    ]
}
EOF
}    


