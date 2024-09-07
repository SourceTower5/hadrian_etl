# Configure the AWS Provider

provider "aws" {
    region = "us-west-1"
    profile = "default"
}

output "aws-region" {
    value = "us-west-1"
    description = "provider region"
}
