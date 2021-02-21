from flask import Flask,render_template, url_for, request , redirect
import boto3
import json
from dateutil.tz import tzutc
import datetime

app=Flask(__name__)

client = boto3.client(  'cloudformation',region_name = "ap-south-1",aws_access_key_id="AKIAIIDW6BTJCV5XSCZA",
        aws_secret_access_key="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")

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('sam.html')

@app.route('/stack', methods=['GET','POST'])
def stack():
    temp = open("awstemplate.json", "r")
    awsTemplate = json.load(temp)
    temp.close()
    awsTemplate["Parameters"]["InstanceType"]["Default"] =  request.form.get("instanceType")
    awsTemplate["Parameters"]["KeyName"]["Default"] = request.form.get("keyPairNameValue")
    awsTemplate["Parameters"]["SSHLocation"]["Default"] = request.form.get("SSHLocation")
    awsTemplate["Parameters"]["DBName"]["Default"] = request.form.get("databaseName")
    awsTemplate["Parameters"]["DBUser"]["Default"] = request.form.get("databaseUser")
    awsTemplate["Parameters"]["DBPassword"]["Default"] = request.form.get("databasePassword")
    awsTemplate["Parameters"]["DBRootPassword"]["Default"] = request.form.get("databaseRootPassword")
    response = client.create_stack(StackName=request.form.get("stackName"),TemplateBody=json.dumps(awsTemplate))
    response = {'StackId': 'arn:aws:cloudformation:ap-south-1:607224909328:stack/Lokes/8758b940-713b-11eb-9661-064537695128', 'ResponseMetadata': {'RequestId': '3186343a-cc37-4b5a-b215-7c492a851736', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '3186343a-cc37-4b5a-b215-7c492a851736', 'content-type': 'text/xml', 'content-length': '376', 'date': 'Wed, 17 Feb 2021 17:05:07 GMT'}, 'RetryAttempts': 0}}
    print(response)
    response1 = client.describe_stacks(StackName=request.form.get("stackName"), NextToken=' ')
    #response1 = {'Stacks': [{'StackId': 'arn:aws:cloudformation:ap-south-1:607224909328:stack/March/64c9afb0-714a-11eb-81c0-02a0212f641c', 'StackName': 'March', 'Description': 'AWS CloudFormation Sample Template AutoScalingMultiAZWithNotifications: Create a multi-az, load balanced and auto-scaled sample web site running on an Apache Web Server. The application is configured to span all Availability Zones in the region and is auto-scaled based on the CPU utilization of the web servers. Notifications will be sent to the operator email address on scaling events. The instances are load balanced with a simple health check against the default web page. **WARNING** This template creates one or more Amazon EC2 instances and an Elastic Load Balancer. You will be billed for the AWS resources used if you create a stack from this template.', 'Parameters': [{'ParameterKey': 'KeyName', 'ParameterValue': 'test'}, {'ParameterKey': 'SSHLocation', 'ParameterValue': '0.0.0.0/0'}, {'ParameterKey': 'DBPassword', 'ParameterValue': '****'}, {'ParameterKey': 'DBName', 'ParameterValue': 'wordpressdb'}, {'ParameterKey': 'DBUser', 'ParameterValue': '****'}, {'ParameterKey': 'DBRootPassword', 'ParameterValue': '****'}, {'ParameterKey': 'InstanceType', 'ParameterValue': 't2.micro'}], 'CreationTime': datetime.datetime(2021, 2, 17, 18, 3, 9, 890000, tzinfo=tzutc()), 'RollbackConfiguration': {}, 'StackStatus': 'CREATE_IN_PROGRESS', 'StackStatusReason': 'User Initiated', 'DisableRollback': False, 'NotificationARNs': [], 'Tags': [], 'EnableTerminationProtection': False, 'DriftInformation': {'StackDriftStatus': 'NOT_CHECKED'}}], 'ResponseMetadata': {'RequestId': '3d868379-6271-4379-a43f-e2aa426a4c79', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '3d868379-6271-4379-a43f-e2aa426a4c79', 'content-type': 'text/xml', 'content-length': '2718', 'vary': 'accept-encoding', 'date': 'Wed, 17 Feb 2021 18:03:09 GMT'}, 'RetryAttempts': 0}}  
    stackId = response1['Stacks'][0]['StackId']
    stackName = response1['Stacks'][0]['StackName']
    description = response1['Stacks'][0]['Description']
    creationTime = response1['Stacks'][0]['CreationTime']
    stackStatus = response1['Stacks'][0]['StackStatus']
    stackStatusReason = response1['Stacks'][0]['StackStatusReason']
    requestId = response1['ResponseMetadata']['RequestId']

    return render_template('stack.html',stackId=stackId,stackName=stackName,creationTime=creationTime,stackStatus=stackStatus,stackStatusReason=stackStatusReason,requestId=requestId,description=description)

if __name__ == "__main__":
    app.run()

