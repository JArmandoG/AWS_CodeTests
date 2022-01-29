import boto3, json

''' USED AS A LOCAL FUNCTION (PC/TERMINAL)

This will simply invoke $lambda_function_name and receive the contents of the
return function

'''

# Payload that will -Return- the lambda function
test_event = dict()

lambda_function_name = ''
lambda_location = ''

lambda_client = boto3.client('lambda',region_name=lambda_location)

response = lambda_client.invoke(
  FunctionName=lambda_function_name,
  Payload=json.dumps(test_event),
)

print(response['Payload'])
print(response['Payload'].read().decode("utf-8"))
