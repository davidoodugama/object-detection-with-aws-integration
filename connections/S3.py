import os
from .secrets123 import aws_access_key, aws_secret_key
import boto3
from const.const import S3,REGION

s3 = boto3.resource(
                    service_name = S3,
                    region_name = REGION,
                    aws_access_key_id = aws_access_key,
                    aws_secret_access_key = aws_secret_key
)
s3_1 = boto3.client(
    service_name = S3,
    region_name = REGION,
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_key
)
os.environ['AWS_DEFAULT_REGION'] = REGION
os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key
os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key