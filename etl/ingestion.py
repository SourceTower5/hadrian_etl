import boto3

def write_to_s3(file_name, bucket_name="jimmy-hadrian-ml-data-bucket"):
    s3 = boto3.client("s3")
    try:
        # TODO create full path to file
        with open(file_name, "rb") as file:
            s3.upload_fileobj(file, bucket_name, file_name)
        print(f"File {file_name} uploaded to S3 bucket {bucket_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Example usage:
write_to_s3("sample_data.csv")