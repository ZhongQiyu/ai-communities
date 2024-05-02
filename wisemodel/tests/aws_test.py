# test_aws.py
import boto3
import os
from botocore.exceptions import NoCredentialsError

def download_from_s3(bucket_name, file_key, download_path):
    """
    从AWS S3下载文件到本地。

    :param bucket_name: S3存储桶的名称
    :param file_key: S3中的文件键（路径）
    :param download_path: 本地文件保存路径
    """
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, file_key, download_path)
        print(f"Successfully downloaded {file_key} from {bucket_name} to {download_path}")
    except NoCredentialsError:
        print("Error: AWS credentials not available")
    except Exception as e:
        print(f"Error downloading file from S3: {e}")

def main():
    # 从环境变量获取AWS凭证
    bucket_name = os.getenv('AWS_BUCKET_NAME')
    file_key = os.getenv('AWS_FILE_KEY')
    download_path = os.getenv('AWS_DOWNLOAD_PATH', 'downloaded_file')

    if not bucket_name or not file_key:
        print("Error: Please set AWS_BUCKET_NAME and AWS_FILE_KEY environment variables")
        return

    download_from_s3(bucket_name, file_key, download_path)

if __name__ == '__main__':
    main()

