import pytest
import os
from utils.minio_client import MinioClient

@pytest.fixture(scope="module")
def minio_client():
    return MinioClient()

@pytest.fixture(scope="module")
def setup_test_data(minio_client):
    # Setup test data
    bucket_name = "test-bucket"
    minio_client.create_bucket(bucket_name)
    print(f"Using bucket: {bucket_name}")
    file_path = os.path.abspath("data/test_data.csv") 
    print("file_path", file_path) # Corrected path
    object_name = "test_data.csv"
    minio_client.upload_file(file_path, bucket_name, object_name)
    return bucket_name, object_name

def test_minio_connection(minio_client):
    """Test MinIO connection and bucket listing"""
    buckets = minio_client.list_buckets()
    assert len(buckets) > 0

def test_products_data(minio_client, setup_test_data):
    """Test products data retrieval and validation"""
    df = minio_client.get_products_data()
    print("df",df.head())
    assert len(df) > 0
    assert 'product_id' in df.columns