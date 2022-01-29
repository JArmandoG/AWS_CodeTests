import json
import requests

''' USED AS A LAMBDA FUNCTION 👍
This will receive a message (remote "event" json object) and forward it 
through the Slack's webhook $url with the $headers set

works with Python3.7, not 3.9 (requests is deprecated and boto does not
support it)
'''

url = ''
headers = {'Content-Type': "application/json"}

def lambda_handler(event, context):
    message = json.dumps(event)
    try:
        req = requests.post(url, data=message, headers=headers)
        if req.status_code == 200:
            Response_body = '[+] Message Sent'
            return {
            'statusCode': 200,
            'body': json.dumps(Response_body)
            }
        else:
            Response_body = '[-] Error ' + str(req.status_code)
            return Response_body
    except Exception as e:
        return str(e)