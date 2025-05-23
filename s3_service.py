from app.config import get_s3_client
import base64
import string
import random

s3 = get_s3_client()

def get_random_string():
    characters = string.ascii_lowercase
    random_string=''.join(random.choices(characters,k=4))
    print(random_string)
    return random_string


def list_buckets():
    return s3.list_buckets().get('Buckets', [])

def list_objects(bucket_name):
    return s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])

def create_bucket(bucket_name):
    response = s3.create_bucket(
            Bucket=bucket_name + get_random_string(),
            CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'}
        )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {f"Bucket {bucket_name} created successfully.!"}
    else:
        return response

def delete_bucket(bucket_name):
    return s3.delete_bucket(Bucket=bucket_name)

def create_folder(bucket_name, folder_name):
    key = folder_name.rstrip("/") + "/"
    return s3.put_object(Bucket=bucket_name, Key=key)

def delete_file(bucket_name, key):
    return s3.delete_object(Bucket=bucket_name, Key=key)

def upload_file(bucket_name, key, content_base64):
    content = base64.b64decode(content_base64.encode())
    return s3.put_object(Bucket=bucket_name, Key=key, Body=content)

def copy_file(source_bucket, source_key, dest_bucket, dest_key):
    copy_source = {'Bucket': source_bucket, 'Key': source_key}
    return s3.copy_object(CopySource=copy_source, Bucket=dest_bucket, Key=dest_key)

def move_file(source_bucket, source_key, dest_bucket, dest_key):
    copy_file(source_bucket, source_key, dest_bucket, dest_key)
    delete_file(source_bucket, source_key)
