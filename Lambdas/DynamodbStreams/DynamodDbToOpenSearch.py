import boto3
import os
import requests
import json
from requests_aws4auth import AWS4Auth

region = 'eu-central-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://' + os.environ['openSearchServiceDomain'] # the OpenSearch Service domain, with https://
index = 'lambda-index'
type = '_doc'
url = host + '/' + index + '/' + type + '/'

headers = { "Content-Type": "application/json" }

def handler(event, context):
    count = 0
    for record in event['Records']:
        # Get the primary key for use as the OpenSearch ID
        id = record['dynamodb']['Keys']['ID']['S']
        
        print(str(record))

        if record['eventName'] == 'REMOVE':
            r = requests.delete(url + id, auth=awsauth)
        else:
            
            document = record['dynamodb']['NewImage']
            
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            boto3.resource('dynamodb')
            
            # To go from low-level format to python
            deserializer = boto3.dynamodb.types.TypeDeserializer()
            python_data = {k: deserializer.deserialize(v) for k,v in document.items()}
            
            # To go from python to low-level format
            # serializer = boto3.dynamodb.types.TypeSerializer()
            # low_level_copy = {k: serializer.serialize(v) for k,v in python_data.items()}
            
            # assert low_level_data == low_level_copy
            
            print('Adding a new item from NewImage: ' + json.dumps(python_data) + '\n')

            r = requests.put(url + id, auth=awsauth, data=json.dumps(python_data), headers=headers)
            print('Response: ' + str(r.content) + '\n')
            print(r.raise_for_status())
            

        count += 1

    print(str(count) + ' records processed.')
    return str(count) + ' records processed.'