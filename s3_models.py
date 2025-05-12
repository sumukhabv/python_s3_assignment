from pydantic import BaseModel

class BucketAction(BaseModel):
    bucket_name: str

class FolderAction(BaseModel):
    bucket_name: str
    folder_name: str

class FileAction(BaseModel):
    bucket_name: str
    file_key: str

class UploadFileAction(BaseModel):
    bucket_name: str
    file_key: str
    file_content: str  # Base64 or plain text

class MoveCopyAction(BaseModel):
    source_bucket: str
    source_key: str
    destination_bucket: str
    destination_key: str
