from moto import mock_aws
from app import lambda_handler
from unittest.mock import patch
import json
import os
import sys
import pytest
import boto3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'


@mock_aws
def test_lambda_handler_success():
    # Set up mock AWS services
    sns = boto3.client('sns')
    s3 = boto3.client('s3')
    
    # Create mock SNS topic
    topic = sns.create_topic(Name='test-topic')
    os.environ['SNS_TOPIC_ARN'] = topic['TopicArn']
    
    # Create mock bucket
    s3.create_bucket(
        Bucket='test-bucket',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )
    
    # Mock Security Hub batch_import_findings call
    with patch('boto3.client') as mock_boto3:
        mock_security_hub = mock_boto3.return_value
        mock_security_hub.batch_import_findings.return_value = {'SuccessCount': 1, 'FailedCount': 0}
        
        # Mock event data
        event = {
            'detail': {
                'id': 'test-finding',
                'region': 'eu-west-2',
                'accountId': '123456789012',
                'resourcesAffected': {
                    's3Bucket': {'name': 'test-bucket'},
                    's3Object': {'key': 'test-object'}
                },
                'severity': {'description': 'HIGH'},
                'description': 'Unencrypted data found'
            }
        }
        
        # Call handler
        response = lambda_handler(event)
        
        # Assert response structure
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == 'Successfully processed Macie finding'

@mock_aws
def test_lambda_handler_invalid_event():
    # Set up AWS region
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'
    
    # Test with invalid event
    with pytest.raises(Exception):
        lambda_handler({})