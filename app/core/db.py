import boto3
from botocore.utils import ClientError
from app.core.logger import logger
from app.core.config import get_settings


settings = get_settings()

def get_dynamodb_client():
    return boto3.client(
        "dynamodb",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    )

def get_dynamodb_resource():
    return boto3.resource(
        "dynamodb",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

def init_dynamodb_table(table_name: str):
    dynamodb = get_dynamodb_resource()
    try:
        table = dynamodb.Table(table_name)
        table.load()
        logger.debug(f"Table '{table_name}' already exists.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            logger.debug(f"Creating table '{table_name}'...")
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "id", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "id", "AttributeType": "N"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            )
            table.wait_until_exists()
            logger.debug(f"Table '{table_name}' created successfully.")
        else:
            logger.error(f"Error creating table '{table_name}': {e}")
            raise

