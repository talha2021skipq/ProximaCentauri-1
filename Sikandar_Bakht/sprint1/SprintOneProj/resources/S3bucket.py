import json
import boto3


class S3Bucket:
    def __init__(self, bucket_name):
        self.bucket = boto3.resource("s3", region_name='us-east-2').Bucket(bucket_name)

    def load(self, key):
        return json.load(self.bucket.Object(key=key).get()["Body"])

    def dump(self, key, obj):
        return self.bucket.Object(key=key).put(Body=json.dumps(obj))


def test_it():
    jsbucket = S3Bucket("your_bucket_name")
    org_data = {"test": 12345}

    jsbucket.dump("test/data.json", org_data)
    read_data = jsbucket.load("test/data.json")
    assert read_data == org_data