import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Создание клиента для работы с MinIO
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',  # URL MinIO
    aws_access_key_id='minioaccesskey',  # Ключ доступа
    aws_secret_access_key='miniosecretkey',  # Секретный ключ
    region_name='us-east-1'  # Регион (можно оставить по умолчанию)
)

bucket_name = 'my-bucket'

try:
    s3.upload_file('online_sales_dataset.csv', bucket_name, 'remote_file.txt')
    print("File uploaded successfully")
except FileNotFoundError:
    print("File not found")
except NoCredentialsError:
    print("Credentials not available")
except ClientError as e:
    print(f"Error uploading file: {e}")
