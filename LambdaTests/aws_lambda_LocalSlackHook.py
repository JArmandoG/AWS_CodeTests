import json
import requests

''' USED AS A LAMBDA FUNCTION

This will send this local $message to Slack's $url hook

'''

message = {"text" : "Hello World"}
url = ''
headers = {'Content-Type': "application/json"}

def lambda_handler(event, context):
    try:
        req = requests.post(url, data=json.dumps(message), headers=headers)
        if req.status_code == 200:
            Response_body = 'Message Sent'
            return {
            'statusCode': 200,
            'body': json.dumps(Response_body)
            }
        else:
            Response_body = '[-] Error ' + str(req.status_code)
            return Response_body
    except Exception as e:
        return str(e)