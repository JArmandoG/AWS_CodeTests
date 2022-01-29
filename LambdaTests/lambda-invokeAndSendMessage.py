import boto3, json

'''
This will send a message ("message") to $lambda_function_name in $lambda_location
as "event" in lambda_handler()
'''

message = {
    "text": "Hello world"
}

lambda_function_name = ''
lambda_location = ''

lambda_client = boto3.client('lambda',region_name=lambda_location)

response = lambda_client.invoke(
  FunctionName=lambda_function_name,
  # JSON object
  Payload=json.dumps(message),
)

print(response['Payload'])
print(response['Payload'].read().decode("utf-8"))