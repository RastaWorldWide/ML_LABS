import boto3
import argparse
from botocore.exceptions import NoCredentialsError, ClientError


def upload_data(bucket_name, file_name, local_path):
    s3 = boto3.client(
        's3',
        endpoint_url='http://localhost:9000',  # URL MinIO
        aws_access_key_id='minioaccesskey',
        aws_secret_access_key='miniosecretkey',
        region_name='us-east-1'
    )

    try:
        # Загружаем файл в S3
        s3.upload_file(local_path, bucket_name, file_name)
        print(f"File {local_path} uploaded successfully to {bucket_name}/{file_name}")
    except NoCredentialsError:
        print("Credentials not available")
    except ClientError as e:
        print(f"Error uploading file: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Upload data to S3")
    parser.add_argument('--bucket', required=True, help="S3 bucket name")
    parser.add_argument('--file', required=True, help="S3 file name")
    parser.add_argument('--local-path', required=True, help="Local path to the file")

    args = parser.parse_args()
    upload_data(args.bucket, args.file, args.local_path)


if __name__ == '__main__':
    main()
