import threading
from threading import Thread
import logging
import boto3
from botocore.config import Config
from config import yotta_upload_endpoint, yotta_download_endpoint, yotta_access_key, yotta_secret_key, yotta_bucket_name, yotta_file_prefix, yotta_region_name, yotta_link_prefix, download_folder
from utilities import post_error
import os


log = logging.getLogger('file')

class AzureFileRepo():
    """
    Yotta S3-compatible file repository.
    Maintains 'AzureFileRepo' naming and method signatures for backward compatibility.
    Routes to Yotta S3-compatible storage using boto3.
    """

    def __init__(self):
        """Initialize separate S3 clients for upload and download operations"""
        # Common configuration for both clients
        s3_config = Config(
            signature_version="s3v4"
        )

        # Upload client (uses upload endpoint)
        self.s3_upload_client = boto3.client(
            's3',
            endpoint_url=yotta_upload_endpoint,
            aws_access_key_id=yotta_access_key,
            aws_secret_access_key=yotta_secret_key,
            config=s3_config,
            region_name=yotta_region_name
        )

        # Download client (uses download endpoint)
        self.s3_download_client = boto3.client(
            's3',
            endpoint_url=yotta_download_endpoint,
            aws_access_key_id=yotta_access_key,
            aws_secret_access_key=yotta_secret_key,
            config=s3_config,
            region_name=yotta_region_name
        )

        log.info(f'Initialized Yotta S3 clients - Bucket: {yotta_bucket_name}, Upload: {yotta_upload_endpoint}, Download: {yotta_download_endpoint}')

    #uploading file to Yotta S3 storage
    def upload_file_to_blob(self, file_path, file_name, folder):
        """
        Upload file to Yotta S3 storage in background thread.

        Args:
            file_path (str): Local path to file to upload
            file_name (str): Name of file
            folder (str): Folder/prefix in bucket

        Returns:
            str: Public URL to uploaded file
        """
        # Construct S3 object key with file prefix
        if yotta_file_prefix:
            # Remove trailing slash from prefix if present, we'll add it back
            prefix = yotta_file_prefix.rstrip('/')
            blob_file_name = f"{prefix}/{folder}/{file_name}"
        else:
            blob_file_name = f"{folder}/{file_name}"

        log.info(f'Pushing {file_path} to Yotta S3 at {blob_file_name} on a new fork......')
        persister = threading.Thread(target=self.upload_file, args=(self.s3_upload_client, file_path, blob_file_name))
        persister.start()
        return f'{yotta_link_prefix}{blob_file_name}'

    #downloading file from Yotta S3 storage
    def download_file_from_blob(self, blob_file_name):
        """
        Download file from Yotta S3 storage.

        Args:
            blob_file_name (str): Full key path in bucket (folder/filename)

        Returns:
            str: Local path to downloaded file, or error dict
        """
        output_filepath = os.path.join(download_folder, blob_file_name)
        try:
            log.info("\nDownloading blob to \n\t" + output_filepath)
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
            self.s3_download_client.download_file(yotta_bucket_name, blob_file_name, output_filepath)
            return output_filepath
        except Exception as e:
            log.exception(e)
            return post_error("Service Exception", f"Exception occurred:{e}")

    #removing file from Yotta S3 storage
    def remove_file_from_blob(self, blob_file_name):
        """
        Remove file from Yotta S3 storage.

        Args:
            blob_file_name (str): Full key path in bucket (folder/filename)

        Returns:
            None on success, error dict on failure
        """
        log.info(f'Deleting {blob_file_name} from Yotta storage......')
        try:
            self.s3_upload_client.delete_object(Bucket=yotta_bucket_name, Key=blob_file_name)
        except Exception as e:
            log.exception(e)
            return post_error("Service Exception", f"Exception occurred:{e}")


    def upload_file(self, s3_client, file_path, blob_file_name):
        """
        Background worker thread for file upload.
        Uploads file to S3 and removes local copy on success.

        Args:
            s3_client: Boto3 S3 client instance
            file_path (str): Local path to file
            blob_file_name (str): S3 object key
        """
        try:
            s3_client.upload_file(file_path, yotta_bucket_name, blob_file_name)
            os.remove(file_path)
            log.info(f'Successfully uploaded and removed local file: {file_path}')
        except Exception as e:
            log.exception(f'Exception while pushing to Yotta S3: {e}', e)
