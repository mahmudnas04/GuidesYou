import boto3
import base64
import json

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # extract the necessary information from the event
    bucket_name = event['bucket_name']
    file_name = event['file_name']
    encoded_file = event['body']  # assuming the base64 encoded pdf is in the request body
    
    # decode the base64-encoded data
    decoded_file = base64.b64decode(encoded_file)
    
    # write the decoded data to a temporary file
    with open('/tmp/' + file_name, 'wb') as f:
        f.write(decoded_file)
    
    # upload the file to the S3 bucket
    s3_client.upload_file('/tmp/' + file_name, bucket_name, file_name)
    
    # create a response object with the 'Access-Control-Allow-Origin' header
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': 'File uploaded successfully'
    }
    
    # return the response object
    return response
