import sys
import os
sys.path.append('notification')

from lambda_wrapper import LambdaWrapper

import boto3


class NotificationService:

    lambda_wrapper = None
    # Initializing the AWS Lambda client with credentials and region information
    def __init__(self):
        lambda_client = boto3.client('lambda',
                                     region_name='eu-central-1',
                                     aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                     aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
        iam_resource = boto3.resource('iam')

        # Creating an instance of LambdaWrapper with the Lambda client and IAM resource
        self.lambda_wrapper = LambdaWrapper(lambda_client, iam_resource)

    # Method to invoke the 'SendEmail' Lambda function with provided parameters
    def send_email(self, params):
        return self.lambda_wrapper.invoke_function('arn:aws:lambda:eu-central-1:471112565104:function:SendEmail', params)

    # Method to invoke the 'ScheduleEvent' Lambda function with provided parameters
    def schedule_email(self, params):
        return self.lambda_wrapper.invoke_function('arn:aws:lambda:eu-central-1:471112565104:function:ScheduleEvent', params)