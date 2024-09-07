import boto3
import logging
import os
logger = logging.getLogger(__name__)


class Ingester:
    def __init__(self, bucket_name="jimmy-hadrian-ml-data-bucket"):
        self.bucket_name = bucket_name
        # initialize s3 client
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        region_name = os.environ.get("REGION_NAME")

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def write_to_s3(self, file_name):
        try:
            logger.info(f"Uploading file {file_name} to S3 bucket {self.bucket_name}")
            
            # Future enhancement: upload data in chunks, support parallell uploads
            with open(file_name, "rb") as file:
                self.s3_client.upload_fileobj(file, self.bucket_name, file_name)

            # Amount of data uploaded

            logger.info(f"File {file_name} uploaded to S3 bucket {self.bucket_name}")
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
