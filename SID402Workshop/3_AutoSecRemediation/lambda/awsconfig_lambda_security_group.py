# Copyright [2016]-[2016] Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
# Description: Checks that all security groups block access to the specified ports.
#
# awscwevents_lambda_security_group.py
#
# Author: jeffscottlevine
# Date: 2016-09-05
#
# This file contains an AWS Lambda handler which responds to AWS API calls that modify the ingress
# permissions of security groups to see if the permissions now differ from the required permissions
# as specificed in the REQUIRED_PERMISSIONS variable below.
#
# Note: The permissions are not remediated within this function because doing so could possibly
# trigger a recursion issue with this Lambda function triggering itself.
#
# 2017-01-13 - Added "Ipv6Ranges" to REQUIRED_PERMISSIONS to accommodate IPv6 within Amazon VPC.

import boto3
import botocore
import json


APPLICABLE_APIS = ["AuthorizeSecurityGroupIngress", "RevokeSecurityGroupIngress"]

# Specify the required ingress permissions using the same key layout as that provided in the
# describe_security_group API response and authorize_security_group_ingress/egress API calls.

REQUIRED_PERMISSIONS = [
{
    "IpProtocol" : "tcp",
    "FromPort" : 80,
    "ToPort" : 80,
    "UserIdGroupPairs" : [],
    "IpRanges" : [{"CidrIp" : "0.0.0.0/0"}],
    "PrefixListIds" : [],
    "Ipv6Ranges": []
},
{
    "IpProtocol" : "tcp",
    "FromPort" : 443,
    "ToPort" : 443,
    "UserIdGroupPairs" : [],
    "IpRanges" : [{"CidrIp" : "0.0.0.0/0"}],
    "PrefixListIds" : [],
    "Ipv6Ranges": []
}]


# evaluate_compliance
#
# This is the main compliance evaluation function.

def evaluate_compliance(event):
    event_name = event["detail"]["eventName"]
    if event_name not in APPLICABLE_APIS:
        print("This rule does not apply for the event ", event_name, ".")
        return

    group_id = event["detail"]["requestParameters"]["groupId"]
    print("group id: ", group_id)

    client = boto3.client("ec2");

    try:
        response = client.describe_security_groups(GroupIds=[group_id])
    except botocore.exceptions.ClientError as e:
        print("describe_security_groups failure on group ", group_id, " .")
        return

    print("security group definition: ", json.dumps(response, indent=2))

    ip_permissions = response["SecurityGroups"][0]["IpPermissions"]
    authorize_permissions = [perm for perm in REQUIRED_PERMISSIONS if perm not in ip_permissions]
    revoke_permissions = [perm for perm in ip_permissions if perm not in REQUIRED_PERMISSIONS]

    if authorize_permissions or revoke_permissions:
        if authorize_permissions:
            for perm in authorize_permissions:
                print("This permission must be authorized: ", json.dumps(perm, separators=(',',':')))
        if revoke_permissions:
            for perm in revoke_permissions:
                print("This permission must be revoked: ", json.dumps(perm, separators=(',',':')))
    else:
        print("All permissions are correct.")

# lambda_handler
#
# This is the main handle for the Lambda function.  AWS Lambda passes the function an event and a context.

def lambda_handler(event, context):
    print("event: ", json.dumps(event))

    evaluation = evaluate_compliance(event)
