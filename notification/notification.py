from lambda_wrapper import LambdaWrapper

import boto3


class NotificationService:

    lambda_wrapper = None

    def __init__(self):
        lambda_client = boto3.client('lambda')
        iam_resource = boto3.resource('iam')

        self.lambda_wrapper = LambdaWrapper(lambda_client, iam_resource)

    def send_email(self, params):
        return self.lambda_wrapper.invoke_function('arn:aws:lambda:eu-central-1:471112565104:function:SendEmail', params)

    def schedule_email(self, params):
        return self.lambda_wrapper.invoke_function('arn:aws:lambda:eu-central-1:471112565104:function:ScheduleEvent', params)