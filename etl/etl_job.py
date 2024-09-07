import boto3
import csv
import logging
import os 
import psycopg2

logger = logging.getLogger(__name__)

class ETL_Upper:
    def __init__(self, bucket_name="jimmy-hadrian-ml-data-bucket"):
        # setup s3 connection
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        region_name = os.environ.get("REGION_NAME")
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

        # setup sql connection
        self.sql_host = os.environ.get("SQL_HOST") # <instance-name>.123456.<region>.rds.amazonaws.com
        self.sql_user = os.environ.get("SQL_USER")
        self.sql_password = os.environ.get("SQL_PASSWORD")
        self.sql_db = os.environ.get("SQL_DB")
        self.sql_table = os.environ.get("SQL_TABLE")

        # Create database connection
        self.sql_connection = psycopg2.connect(
            host=self.sql_host,
            user=self.sql_user,
            password=self.sql_password,
            database=self.sql_db,
            connect_timeout=10
        )

        self.local_file = ""

    def __del__(self):
        self.sql_connection.close()

    def download_data(self, file_name):
        # Process the data
        """
        Downloads data from an S3 file and returns it as a list of CSV rows.

        :param file_name: The path to the S3 file to download
        :return: A list of CSV rows
        """
        # Download data from the S3 bucket and save into tmp
        self.local_file = f"/tmp/{file_name}"

        # get local folder path
        local_folder_path = os.path.split(self.local_file)[0]
        # create local folder if not exists
        os.makedirs(local_folder_path, exist_ok=True)

        try:
            self.s3_client.download_file(self.bucket_name, file_name, self.local_file)
        except Exception as e:
            logger.error(f"Error downloading file: {e}")

        with open(self.local_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
        return rows


    def transform_data_all_upper(self):
        with open(self.local_file, 'r') as f:
            lines = f.readlines()

        with open(self.local_file, 'w') as f:
            f.write(lines[0])  # Write the first line as is
            for line in lines[1:]:
                f.write(line.upper())  # Write the rest of the lines in upper case


    def upload_csv_to_sql(self):
        # create load query from template
        load_query = """
        COPY {sql_table} FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE AS '\"' ;
        """.format(
            sql_table=self.sql_table
        )

        # create sql cursor
        sql_cursor = self.sql_connection.cursor()

        # execute load query
        try:
            logger.info(f"Drop table: {self.sql_table}")
            sql_cursor.execute("""
                DROP TABLE IF EXISTS {sql_table}
            """.format(sql_table=self.sql_table))


            logger.info(f"Creating table if not exists: {self.sql_table}")
            sql_cursor.execute("""
                CREATE TABLE IF NOT EXISTS {sql_table}(           
                id integer PRIMARY KEY,
                Name text,
                Superpower text,
                Affiliation text
            )
            """.format(sql_table=self.sql_table))
            
            logger.info(f"Executing load query: {load_query}")

            with open(self.local_file, mode='r') as local_file:
                sql_cursor.copy_expert(sql=load_query, file=local_file)

            logger.info("Load query completed")
            self.sql_connection.commit()

        except Exception as load_exception:
            self.sql_connection.rollback()

            # close sql cursor and connection
            sql_cursor.close()

            logger.error(f"Error executing load query: {load_exception}")
            raise Exception("SQL LOAD error: " + str(load_exception)) from load_exception
        
        # close sql cursor and connection
        sql_cursor.close()

    def print_records(self):
        sql_cursor = self.sql_connection.cursor()
        sql_cursor.execute("SELECT * from {sql_table}".format(sql_table=self.sql_table))
        records = sql_cursor.fetchall()
        print (f"records: {records}")

        sql_cursor.close()