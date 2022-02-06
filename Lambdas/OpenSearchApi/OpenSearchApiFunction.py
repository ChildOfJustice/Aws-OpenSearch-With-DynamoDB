import boto3
import os
import json
import requests
from requests_aws4auth import AWS4Auth

region = 'eu-central-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://' + os.environ['openSearchServiceDomain'] # the OpenSearch Service domain, with https://
index = 'lambda-index'
type = '_search'
search_url = host + '/' + index + '/' + type + '/'

headers = { "Content-Type": "application/json" }

def handler(event, context):
    body_object = event.get('body')


    print("request: " + str(body_object.get("opensearchQuery")))
    response = requests.post(search_url, auth=awsauth, data=json.dumps(body_object.get("opensearchQuery")), headers=headers)
    print('Response: ' + str(response.json()) + '\n')

    response_object = response.json()

    found_data = response_object.get("hits").get("hits") # "hits" array

    print("DATA:")
    print(str(found_data))
    
    response = {
        'statusCode': 200,
        'body': json.dumps(found_data),
    }
    return response
# TEST event:
# {
#   "body": {
#     "opensearchQuery": {
#       "query": {
#           "bool": {
#               "must": [{"match":{
#                   "tag" : {
#                     "S" : "Tag2Value"
#                   }
#               }}]
#           }
        
#       }
#     }
#   }
# }