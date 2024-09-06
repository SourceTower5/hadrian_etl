import boto3
import csv

# Connect to the RDS instance
rds_client = boto3.client("rds")
db_instance = "example-rds"
db_username = "admin"
db_password = "admin"

# Connect to the S3 bucket
s3_client = boto3.client("s3")
bucket_name = "jimmy-hadrian-ml-data-bucket"

# Download data from the S3 bucket
s3_key = "sample_data.csv"
s3_file = f"/tmp/{s3_key}"
s3_client.download_file(bucket_name, s3_key, s3_file)

# Process the data
with open(s3_file, "r") as file:
    reader = csv.reader(file)
    rows = list(reader)
    # Perform simple transformation on the data
    for row in rows:
        row[0] = row[0].replace("Avengers", "X-Men")

# Upload the processed data to the RDS instance
db_secret_name = "example-rds-secret"
db_secret = rds_client.describe_db_secrets.SecretList()[0]["Secrets"][0]
db_secret_arn = db_secret["SecretArn"]
rds_client.execute_database_query(
    DBName=db_instance,
    SecretArn=db_secret_arn,
    Query=f"INSERT INTO marvel_characters ({', '.join(['col' + str(i) for i in range(len(rows[0]))])}) VALUES ({', '.join(['%s' for _ in range(len(rows[0]))])})",
    Parameters="(" + ", ".join(["%s" for _ in range(len(rows[0]))]) + ")",
    SqlTimeout=5,
    AutoExecute=True,
)
for row in rows:
    rds_client.execute_statement(
        secretArn=db_secret_arn,
        database=db_instance,
        resourceArn=f"arn:aws:rds:us-west-1:{rds_client.meta.account_id}:db:{db_instance}",
        statementId="insert-row",
        parameters=row,
        sql="INSERT INTO marvel_characters ({0}) VALUES ({1})".format(
            ", ".join([col for col in row]),
            ", ".join(["%s" for _ in range(len(row))]),
        ),
    )