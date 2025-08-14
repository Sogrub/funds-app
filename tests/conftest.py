import sys
import os

from app.core.config import Settings

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)

import pytest
from fastapi.testclient import TestClient
from app.main import app
from moto import mock_aws
import boto3
from app.core.db import get_dynamodb_resource

TABLES = ["users", "funds", "subscriptions", "transactions"]

settings = Settings()

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")
def mock_dynamodb_resource():
    with mock_aws():
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="us-east-1",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        for table_name in TABLES:
            dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "N"}],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            ).wait_until_exists()

        yield dynamodb

@pytest.fixture(scope="session", autouse=True)
def clean_dynamodb():
    dynamodb = get_dynamodb_resource()
    for table_name in TABLES:
        try:
            table = dynamodb.Table(table_name)
            items = table.scan().get("Items", [])
            with table.batch_writer() as batch:
                for item in items:
                    batch.delete_item(Key={"id": item["id"]})
        except dynamodb.meta.client.exceptions.ResourceNotFoundException:
            pass
    yield