import boto3
from minio import Minio
import pandas as pd
from botocore.client import Config
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MinioClient:
    def __init__(self):
        # Get MinIO configuration from environment variables
        self.endpoint = os.environ.get('MINIO_ENDPOINT')
        self.access_key = os.environ.get('MINIO_ACCESS_KEY')
        self.secret_key = os.environ.get('MINIO_SECRET_KEY')
        self.bucket_name = os.environ.get('MINIO_BUCKET')
        self.file_path = os.environ.get('MINIO_PRODUCTS_KEY')
        print(f"Connecting to MinIO at: {self.endpoint}")
        
        if not all([self.endpoint, self.access_key, self.secret_key]):
            raise ValueError("Missing required MinIO configuration in environment variables")
        
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False
        )


    def list_buckets(self):
        """List all buckets in MinIO"""
        try:
            print("State client", self.client)
            response = self.client.list_buckets()
            print("Response", response)
            return [bucket for bucket in response]
        except Exception as e:
            raise Exception(f"Failed to list buckets: {str(e)}")
    
    def get_products_data(self):
        """Retrieve products data from MinIO"""
        try:
            response = self.client.get_object(
                self.bucket_name,
                self.file_path
            )
            # Read the content of the response
            return pd.read_csv(BytesIO(response.data))
        except Exception as e:
            raise Exception(f"Failed to retrieve products data: {str(e)}")
    
    def create_bucket(self, bucket_name):
        """Create a new bucket if it doesn't exist"""
        try:
            if bucket_name not in self.list_buckets():
                self.client.make_bucket(bucket_name)
                print(f"Bucket {bucket_name} created successfully")
        except Exception as e:
            raise Exception(f"Failed to create bucket: {str(e)}")

    def upload_file(self, file_path, bucket_name, object_name):
        """Upload a file to MinIO"""
        try:
            self.create_bucket(bucket_name)
            with open(file_path, "rb") as file_data:  # Open the file in binary read mode
                file_stat = os.stat(file_path)  # Get the file size
                self.client.put_object(
                    bucket_name,
                    object_name,
                    file_data,
                    file_stat.st_size,  # Pass the file size
                    content_type="application/csv",
                )
            print(f"File uploaded successfully to {bucket_name}/{object_name}")
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")