import streamlit as st
import requests
import base64
import pandas as pd

API_URL = "http://localhost:8000/s3"  # FastAPI must be running

st.set_page_config(page_title="S3 File Manager", layout="centered")
st.title("🗂️ AWS S3 File Manager")

st.sidebar.header("Operations")
operation = st.sidebar.radio("Select Operation", [
    "List Buckets", "Create Bucket", "Delete Bucket",
    "List Objects", "Create Folder", "Upload File",
    "Delete File", "Copy File", "Move File"
])


def list_buckets():
    resp = requests.get(f"{API_URL}/buckets")

    # Convert the JSON response to a list of dictionaries (if it isn't already)
    data = resp.json()

    # Display header
    st.subheader("Available Buckets:")

    # Convert to a DataFrame for tabular display
    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)
        st.table(df)  # You can also use st.dataframe(df) for a scrollable, interactive version
    else:
        st.write("No buckets found or unexpected data format.")


def create_bucket():
    bucket = st.text_input("Enter unique bucket name")
    if st.button("Create"):
        resp = requests.post(f"{API_URL}/bucket/create", json={"bucket_name": bucket})
        st.success("Bucket created!" if resp.status_code == 200 else resp.text)


def delete_bucket():
    bucket = st.text_input("Enter bucket name to delete")
    if st.button("Delete"):
        resp = requests.post(f"{API_URL}/bucket/delete", json={"bucket_name": bucket})
        st.success("Bucket deleted!" if resp.status_code == 200 else resp.text)


def list_objects():
    bucket = st.text_input("Bucket name to list objects")
    
    if st.button("List Objects"):
        resp = requests.get(f"{API_URL}/objects/{bucket}")
        
        if resp.status_code == 200:
            objects = resp.json()
            st.subheader(f"Objects in {bucket}:")

            simplified_data = []

            for obj in objects:
                key = obj.get("Key", "")
                
                if key.endswith("/"):
                    object_type = "Folder"
                    object_name = key.rstrip("/")
                elif "/" in key:
                    object_type = f"File in folder {key.split("/")[:-1]}"
                    object_name = key.split("/")[-1]
                else:
                    object_type = "File"
                    object_name = key

                simplified_data.append({
                    "Object Name": object_name,
                    "Object Type": object_type
                })

            # Convert to DataFrame and display as a table
            df = pd.DataFrame(simplified_data)
            st.table(df)
        else:
            st.error(f"Failed to retrieve objects. Status code: {resp.status_code}")


def create_folder():
    bucket = st.text_input("Bucket name")
    folder = st.text_input("Folder name")
    if st.button("Create Folder"):
        resp = requests.post(f"{API_URL}/folder/create", json={
            "bucket_name": bucket,
            "folder_name": folder
        })
        st.success("Folder created!" if resp.status_code == 200 else resp.text)


def upload_file():
    bucket = st.text_input("Bucket name")
    uploaded_file = st.file_uploader("Choose file")
    if uploaded_file and bucket:
        content = base64.b64encode(uploaded_file.read()).decode()
        file_key = uploaded_file.name
        resp = requests.post(f"{API_URL}/file/upload", json={
            "bucket_name": bucket,
            "file_key": file_key,
            "file_content": content
        })
        st.success("File uploaded!" if resp.status_code == 200 else resp.text)


def delete_file():
    bucket = st.text_input("Bucket name")
    file_key = st.text_input("File key to delete")
    if st.button("Delete File"):
        resp = requests.post(f"{API_URL}/file/delete", json={
            "bucket_name": bucket,
            "file_key": file_key
        })
        st.success("File deleted!" if resp.status_code == 200 else resp.text)


def copy_file():
    st.subheader("Copy File")
    src_bucket = st.text_input("Source Bucket")
    src_key = st.text_input("Source File Key")
    dest_bucket = st.text_input("Destination Bucket")
    dest_key = st.text_input("Destination File Key")
    if st.button("Copy File"):
        resp = requests.post(f"{API_URL}/file/copy", json={
            "source_bucket": src_bucket,
            "source_key": src_key,
            "destination_bucket": dest_bucket,
            "destination_key": dest_key
        })
        st.success("File copied!" if resp.status_code == 200 else resp.text)


def move_file():
    st.subheader("Move File")
    src_bucket = st.text_input("Source Bucket")
    src_key = st.text_input("Source File Key")
    dest_bucket = st.text_input("Destination Bucket")
    dest_key = st.text_input("Destination File Key")
    if st.button("Move File"):
        resp = requests.post(f"{API_URL}/file/move", json={
            "source_bucket": src_bucket,
            "source_key": src_key,
            "destination_bucket": dest_bucket,
            "destination_key": dest_key
        })
        st.success("File moved!" if resp.status_code == 200 else resp.text)


# Dispatcher
if operation == "List Buckets":
    list_buckets()
elif operation == "Create Bucket":
    create_bucket()
elif operation == "Delete Bucket":
    delete_bucket()
elif operation == "List Objects":
    list_objects()
elif operation == "Create Folder":
    create_folder()
elif operation == "Upload File":
    upload_file()
elif operation == "Delete File":
    delete_file()
elif operation == "Copy File":
    copy_file()
elif operation == "Move File":
    move_file()
