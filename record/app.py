"""Lambda function for recording race records to s3"""
import json
import logging
import uuid
from urllib import parse
import boto3
import requests

BUCKET_NAME = "race-records"
MESSAGES = {'errors': []}
LOCAL = True
S3 = boto3.resource("s3")


def lambda_handler(event, context):
    """Handler"""
    try:
#        obj = json.loads(str(event['body']).encode('utf-8'))
        obj = parse_qs(event['body'])
        file_id = str(uuid.uuid4())
        file_name = file_id + ".json"
        # lambda_path = "records/save"
        name = obj['name']

        if record_exist(name):
            logging.info('Record exist')
            return response()

        logging.info('updating')
        push_to_s3(file_name, obj)
        update_index(file_id, name)
    except requests.RequestException as exception:
        # Send some context about this error to Lambda Logs
        raise exception
    return response()

def parse_qs(query):
    """Parse the query string"""
    query = parse.parse_qs(query, 'true')
    for key, value in query.items():
        query[key] = value[0]
    return query

def response():
    """Return a json response"""
    return {
        "statusCode": 200,
        "body": json.dumps(
            MESSAGES
        ),
    }

def get_index():
    """Get the index.json file and return the body as json"""
    index = read_from_s3('index.json')
    return json.loads(index['Body'].read().decode('utf-8'))

def record_exist(key):
    """Check for the record name in the index"""
    content = get_index()
    try:
        content[key]
    except KeyError:
        return False
    else:
        MESSAGES['errors'].append('Record already exist')
        return True

def s3_path(file_name):
    """Set the s3 object path"""
    return "records/" + file_name

def push_to_s3(file_name, content):
    """Push object to S3 bucket"""
    MESSAGES['info'] = 'Pushed to S3'
    S3.Bucket(BUCKET_NAME).put_object(Key=s3_path(file_name), Body=json.dumps(content))

def update_index(record_id, key):
    """Append new record to index"""
    content = get_index()
    content[key] = record_id
    push_to_s3('index.json', content)

def read_from_s3(file_name):
    """Read file from s3"""
    obj = S3.Object(BUCKET_NAME, s3_path(file_name))
    return obj.get()

#lambda_handler(open('example.json', 'r').read(), '')
