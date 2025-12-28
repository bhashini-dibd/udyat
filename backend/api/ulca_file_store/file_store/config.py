import os

#service configs
DEBUG           =    False
CONTEXT_PATH    =    "/ulca/file-store"
HOST            =   '0.0.0.0'
PORT            =   5001
ENABLE_CORS     =   False
download_folder         =   'downloads/'
object_store            =   os.environ.get('ULCA_OBJECT_STORE', "AZURE")      
shared_storage_path     =   os.environ.get('ULCA_SHARED_STORAGE_PATH', "opt")

#aws configs
aws_file_prefix         =   os.environ.get('ULCA_AWS_FILE_PREFIX',"errors/")
aws_access_key          =   os.environ.get('ULCA_AWS_S3_ACCESS_KEY', 'access-key')
aws_secret_key          =   os.environ.get('ULCA_AWS_S3_SECRET_KEY', 'secret-key')
aws_bucket_name         =   os.environ.get('ULCA_AWS_BUCKET_NAME', 'ulca-datasets')
aws_link_prefix         =   f'https://{aws_bucket_name}.s3.amazonaws.com/'

#yotta s3-compatible configs (replaces azure)
yotta_upload_endpoint   =   os.environ.get('ULCA_YOTTA_UPLOAD_ENDPOINT_URL', 'https://sosnm1.shakticloud.ai:9024')
yotta_download_endpoint =   os.environ.get('ULCA_YOTTA_DOWNLOAD_ENDPOINT_URL', 'https://bhashinimigrationns.sosnm1.shakticloud.ai:9024/')
yotta_access_key        =   os.environ.get('ULCA_YOTTA_ACCESS_KEY', 'access-key')
yotta_secret_key        =   os.environ.get('ULCA_YOTTA_SECRET_KEY', 'secret-key')
yotta_bucket_name       =   os.environ.get('ULCA_YOTTA_BUCKET_NAME', 'ulcauatdsamba')
yotta_region_name       =   os.environ.get('ULCA_YOTTA_REGION_NAME', 'us-east-1')
yotta_link_prefix       =   f'{yotta_download_endpoint}/{yotta_bucket_name}/'




