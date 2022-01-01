import json
import boto3


class S3Bucket:
    '''provides simple API to retrieve and save a json file to an S3 bucket'''
    def __init__(self, bucket_name):
        self.bucket = boto3.resource("s3", region_name='us-east-2').Bucket(bucket_name)

    def load(self, key):
        return json.load(self.bucket.Object(key=key).get()["Body"])

    def dump(self, key, obj):
        return self.bucket.Object(key=key).put(Body=json.dumps(obj))
