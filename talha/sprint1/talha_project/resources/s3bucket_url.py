#s3bucket_url
import aws_cdk.aws_s3 as s3 
class my_s3():
    def __init__(self):
        bucket_talha= s3.Bucket(self, "talha_first_bucket")
        
