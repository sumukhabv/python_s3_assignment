from fastapi import APIRouter
from app.services import s3_service
from app.models.s3_models import *

router = APIRouter()

@router.get("/buckets")
def get_buckets():
    return s3_service.list_buckets()

@router.get("/objects/{bucket_name}")
def get_objects(bucket_name: str):
    return s3_service.list_objects(bucket_name)

@router.post("/bucket/create")
def create_bucket(data: BucketAction):
    return s3_service.create_bucket(data.bucket_name)

@router.post("/bucket/delete")
def delete_bucket(data: BucketAction):
    return s3_service.delete_bucket(data.bucket_name)

@router.post("/folder/create")
def create_folder(data: FolderAction):
    return s3_service.create_folder(data.bucket_name, data.folder_name)

@router.post("/file/delete")
def delete_file(data: FileAction):
    return s3_service.delete_file(data.bucket_name, data.file_key)

@router.post("/file/upload")
def upload_file(data: UploadFileAction):
    return s3_service.upload_file(data.bucket_name, data.file_key, data.file_content)

@router.post("/file/copy")
def copy_file(data: MoveCopyAction):
    return s3_service.copy_file(data.source_bucket, data.source_key, data.destination_bucket, data.destination_key)

@router.post("/file/move")
def move_file(data: MoveCopyAction):
    return s3_service.move_file(data.source_bucket, data.source_key, data.destination_bucket, data.destination_key)
