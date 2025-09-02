
// this is a terraform file:

terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 6.0"
        }
    }
}


provider "aws" {
    profile = "default"
    region = "eu-west-3"
}


