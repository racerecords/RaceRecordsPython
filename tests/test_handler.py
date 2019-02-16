"""Testing S3 lambada function"""
import json
import boto3
import pytest
from moto import mock_s3
from record import app

EXAMPLE = 'bb85bfc0-225f-4ac1-99cc-716db2641177'

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    return {'httpMethod': 'POST',
            'body': "name=test_name&\
                    weather=asdf&\
                    temperature=&\
                    humidity=&\
                    barometer=&\
                    windSpeed=&\
                    windDirection=&\
                    group=&\
                    track=&\
                    region=&\
                    date=&\
                    session=&\
                    start=&\
                    end=&\
                    classes=&\
                    ambientBefore=&\
                    reader=&\
                    recorder=&\
                    siteCertificationDate=&\
                    factoryCalibrationDate=&\
                    fieldCalibrationTime=&\
                    batteryLevel=&\
                    microphoneLocation=",
            'resource': '/record'
            }

@pytest.fixture()
def fixture_record():
    """Fixture for a record"""
    return {"name": "example",
            "weather": "Clear",
            "temperature": "70",
            "humidity": "60",
            "barometer": "30",
            "windSpeed": "2",
            "windDirection": "South",
            "group": "10",
            "track": "DMV",
            "region": "DC",
            "date": "2018-07-01",
            "session": "3",
            "start": "2018-07-01T13:00",
            "end": "2018-07-01T16:00",
            "classes": "A,B",
            "ambientBefore": "20",
            "reader": "Me",
            "recorder": "Myself",
            "siteCertificationDate": "2018-05-30",
            "factoryCalibrationDate": "2010-05-20",
            "fieldCalibrationTime": "2018-07-01T12:00",
            "batteryLevel": "100",
            "microphoneLocation": "Finish Line"
            }

@pytest.fixture()
def fixture_bucket(fixture_record):
    """Fixture for index.json"""
    mock = mock_s3()
    mock.start()
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='race-records')
    index = {
        'example': EXAMPLE,
        'test': '72443892-7cbf-4422-beba-58e046322340',
        'test3': '235eabc7-46ff-4373-8b7e-bbd054bd3fda',
        'test4': '6ea39e8f-6826-426d-b7ff-b3e100cb6cdf',
    }
    conn.Object('race-records', 'records/index.json').put(Body=json.dumps(index))
    conn.Object('race-records', "records/%s.json" %(EXAMPLE)).put(Body=json.dumps(fixture_record))
    yield
    mock.stop()

def test_parse_qs(apigw_event):
    """Put object"""
    res = app.parse_qs(apigw_event['body'])

    assert isinstance(res, dict)
    assert res['name'] == 'test_name'

def test_get_index(fixture_bucket):
    """Should read the index.json"""
    fixture_bucket
    res = app.get_index()

    assert res['example'] == EXAMPLE

def test_record_exist(fixture_bucket):
    """Should return boolean value"""
    fixture_bucket

    assert app.record_exist('example')
    assert not app.record_exist('does_not_exist')

@mock_s3
def test_push_to_s3():
    """Should put object in s3 as json"""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='race-records')
    app.push_to_s3('test', {'json':'test content'})
    body = conn.Object('race-records', 'records/test').get()['Body'].read().decode()

    assert 'test content' in body
    assert isinstance(json.loads(body), dict)
