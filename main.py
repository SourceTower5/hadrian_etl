


from etl.etl_job import ETL_Upper
from etl.ingestion import Ingester


def main():
    ingester = Ingester("jimmy-hadrian-ml-data-bucket")
    ingester.write_to_s3("data/sample_data.csv")
    
    etl = ETL_Upper("jimmy-hadrian-ml-data-bucket")
    etl.download_data("data/sample_data.csv")
    etl.transform_data_all_upper()
    etl.upload_csv_to_sql()
    etl.print_records()

    print("ETL Job Complete!")

if __name__ == '__main__':
    main()

