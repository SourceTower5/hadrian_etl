
# Install libraries

```
sudo apt-get update
sudo apt install postgresql
sudo apt install libpq-dev
sudo apt-get install gcc
pip install boto3
pip install psycopg2
```

# Credentials setup

Create a aws credentials file

~/.aws/credentials

[default]
aws_access_key_id={access}
aws_secret_access_key={secret}

In `provider.tf`, it will reference the default credentials

`profile = "default"`

# Terraform setup

Execute `terraform init` in each of the directories under terraform
```
cd terraform
terraform validate
terraform plan
terraform apply
```


# Executing ingestion

Execute with the credentials set as environment variables

```
# Example usage:
AWS_ACCESS_KEY_ID={} AWS_SECRET_ACCESS_KEY={} REGION={} SQL_HOST={} SQL_USER={} SQL_PASSWORD={} SQL_DB={} SQL_TABLE={} /bin/python3 main.py
```