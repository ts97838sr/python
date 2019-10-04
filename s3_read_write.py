import boto3,os
from boto3.s3.transfer import S3Transfer

class S3_Read_Write():
    """
    Sample function calls :
    read_s3('BucketName','FileName')
    upload_to_s3('LOCALPATH','BucketName','/')
    """
    def read_s3(bucket_name,file_name):
        s3 = boto3.client('s3')
        data = s3.get_object(Bucket=bucket_name,Key=file_name)
        contents = data['Body'].read()
        return contents

    def upload_to_s3(local_path,file_name,bucket_name,s3_path):
        """
        Parameter description
        Filename(str) -- File to be uploaded
        Bucket(str) -- Target Bucket Name
        Key(str) -- The name of the Key(taget File)
        ExtraArgs(dict) -- Additional Argument for Encryption
        """
        s3 = boto3.resource('s3')
        try:
            s3.meta.client.upload_file(local_path,bucket_name,s3_path,ExtraArgs={'ServerSideEncryption': 'AES256', 'ACL': 'bucket-owner-read'})
        except(Exception,boto3.exception.S3UploadFailedError) as error:
            return error
        else:
            "File Upload Successful"
        return 0
