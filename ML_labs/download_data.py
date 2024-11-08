import boto3
import argparse
from botocore.exceptions import NoCredentialsError, ClientError


def download_data(bucket_name, file_name, local_path):
    s3 = boto3.client(
        's3',
        endpoint_url='http://localhost:9000',  # URL MinIO
        aws_access_key_id='minioaccesskey',
        aws_secret_access_key='miniosecretkey',
        region_name='us-east-1'
    )

    try:
        # Скачиваем файл из S3
        s3.download_file(bucket_name, file_name, local_path)
        print(f"File {file_name} downloaded successfully to {local_path}")
    except NoCredentialsError:
        print("Credentials not available")
    except ClientError as e:
        print(f"Error downloading file: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Download data from S3")
    parser.add_argument('--bucket', required=True, help="S3 bucket name")
    parser.add_argument('--file', required=True, help="S3 file name")
    parser.add_argument('--local-path', required=True, help="Local path to save the file")

    args = parser.parse_args()
    download_data(args.bucket, args.file, args.local_path)


if __name__ == '__main__':
    main()
