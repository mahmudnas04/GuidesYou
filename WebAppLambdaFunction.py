import json
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def listObjectsInBucket(BucketName):
    objects = s3.list_objects_v2(Bucket=BucketName)
    if 'Contents' in objects:
        return objects
    else:
        return None
def createPresignedURL(objectList,bucket_name):
    urls = {}
    try:
       

        for obj in objectList['Contents']:
            # print("object is", obj['Key'])
            url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': obj['Key']})
            # print(url)
            urls[obj['Key']] = url
    except ClientError as e:
        logging.error(e)
        return None
    
    return urls
        
def lambda_handler(event, context):
    # bucket_name = event['BucketName']
    # name = "hunter-csci-"+event['BucketName']
    bucket_name = "hunter-csci-"+event['BucketName']
    # print(name)
    list_objects = listObjectsInBucket(bucket_name)
    if list_objects != None:
        urls = createPresignedURL(list_objects,bucket_name)
        if urls != None:
            response = {
                'urls': urls
            }
        else:
            response = None
    
    else:
        response = None
    
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            }
        }
