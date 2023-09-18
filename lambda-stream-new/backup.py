import os
import json
import boto3

def lambda_handler(event, context):
    # Initialize AWS clients for CloudWatch Logs and S3
    cloudwatch_logs = boto3.client('logs')
    s3 = boto3.client('s3')

    # Specify your S3 bucket name and CloudWatch Log Group name
    bucket_name = 'aws-lambda-pmg-s3'
    log_group_name = 'aws-lambda-pmg-loggroup'

    # Retrieve CloudWatch Log Streams 
    log_streams = cloudwatch_logs.describe_log_streams(
        logGroupName=log_group_name,
        orderBy='LastEventTime',
        descending=True
    )

    for stream in log_streams['logStreams']:
        stream_name = stream['logStreamName']

        # Retrieve CloudWatch Log Events for the Log Stream
        log_events = cloudwatch_logs.get_log_events(
            logGroupName=log_group_name,
            logStreamName=stream_name,
            startFromHead=True
        )

        # Prepare the log events for S3 storage
        s3_data = '\n'.join([event['message'] for event in log_events['events']])

        # Upload log events to S3 bucket
        s3_key = f'cloudwatch_logs/{stream_name}.log'  # Replace with your desired S3 key structure
        s3.put_object(Body=s3_data, Bucket=bucket_name, Key=s3_key)
        
        return {
        'statusCode': 200,
        'body': json.dumps('CloudWatch logs collected and stored in S3')
    }