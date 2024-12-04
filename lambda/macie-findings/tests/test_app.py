import json
from datetime import datetime
import pytest
from app import lambda_handler

def test_lambda_handler_success():
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

def test_lambda_handler_invalid_event():
    # Test with invalid event
    with pytest.raises(Exception):
        lambda_handler({})