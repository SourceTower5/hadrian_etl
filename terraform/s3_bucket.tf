# Create an S3 bucket
resource "aws_s3_bucket" "jimmy_hadrian_ml_data_bucket" {
  bucket = "jimmy-hadrian-ml-data-bucket"
}

resource "aws_s3_bucket_versioning" "versioning_jimmy_hadrian_ml_data_bucket" {
  bucket = aws_s3_bucket.jimmy_hadrian_ml_data_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}