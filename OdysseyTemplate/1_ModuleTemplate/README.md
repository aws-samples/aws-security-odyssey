# AWS Security Odyssey - Title

# Module 1 - Sample Module

### Overview

Add the narrative and context describing how this module fits into the flow of the overall workshop / bootcamp.

Provide a high level overview of the module and what will be learned / accomplished.

The module walks you through the process of creating alerts for one such event using AWS Console. Steps for the rest of the events have been automated in a CloudFormation template, which is provided to you.

The module makes use of a number of AWS services namely AWS Identity and Access Management (IAM), AWS CloudTrail, AWS CloudWatch Alarms,  AWS CloudFormation and others.

### Topics Covered

After completing this module, you should be able to automate notifications for any of the below use cases:
- Amazon S3 Bucket Activity
- Security Group Configuration Changes
- Network Access Control List (ACL) Changes
- Network Gateway Changes
- Amazon Virtual Private Cloud (VPC) Changes
- Amazon EC2 Instance Changes
- CloudTrail Changes
- Console Sign-In Failures
- Authorization Failures
- IAM Policy Changes

### Prerequisites

This module is targeted for IT security focused individuals who are interested in learning about automating security related events on AWS. You will need an AWS account with administrators access.

To successfully complete this module, you should be familiar with AWS services including Amazon EC2, S3, VPC etc. and have a basic understanding of security groups, Network Access Control List (NACL), IAM Policies etc. You should be comfortable logging into and using the AWS Management Console and have familiarity with AWS Identity and Access Management (IAM).

### 1. Select a Region and Launch CloudFormation Stack

**Tip** The AWS region name is always listed in the upper-right corner of the AWS Management Console, in the navigation bar.

Make a note of the AWS *region name*, for example, *US West (Oregon),*

For more information about regions, see: [AWS Regions and Endpoints](http://docs.aws.amazon.com/general/latest/gr/rande.html)

**Note** If needed, create a new key pair: [Creating a Key Pair Using Amazon EC2](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair)

##### Launch the CloudFormation Stack in the preferred region:

___Hold the "Control" key while clicking and open the launch link in a new tab___

Region| Launch
------|-----
N. Virginia (us-east-1) | [![Launch Module in us-east-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=SID402-AutomatingSecurityEvents&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/templates/AutomatingSecurityEvents.json)
Ohio (us-east-2) | [![Launch Module in us-east-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=SID402-AutomatingSecurityEvents&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/templates/AutomatingSecurityEvents.json)
Oregon (us-west-2) | [![Launch Module in us-west-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=SID402-AutomatingSecurityEvents&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/templates/AutomatingSecurityEvents.json)
Singapore (ap-southeast-1) | [![Launch Module in ap-southeast-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=SID402-AutomatingSecurityEvents&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/templates/AutomatingSecurityEvents.json)
Sydney (ap-southeast-2) | [![Launch Module in ap-southeast-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=SID402-AutomatingSecurityEvents&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/templates/AutomatingSecurityEvents.json)
Tokyo (ap-northeast-1) | [![Launch Module in ap-northeast-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=SID402-AutomatingSecurityEvents&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/templates/AutomatingSecurityEvents.json)
Seoul (ap-northeast-2) | [![Launch Module in ap-northeast-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=SID402-AutomatingSecurityEvents&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/templates/AutomatingSecurityEvents.json)
Ireland (eu-west-1) | [![Launch Module in eu-west-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=SID402-AutomatingSecurityEvents&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/templates/AutomatingSecurityEvents.json)
London (eu-west-2) | [![Launch Module in eu-west-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=SID402-AutomatingSecurityEvents&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/templates/AutomatingSecurityEvents.json)

1. On the Select Template screen, click **Next**.
2. On the Specify Details page, provide the key pair that you plan to use and your public IP range from which you will initiate SSH connections.
3. Click Next.
4. On the Options page, you can create tags or configure other advanced options. These are not required for this module.
5. Click **Next**.
6. On the Review page, verify that the template, key pair, SSH CIDR range, and other options, if any, are correct.
7. Select **I acknowledge that AWS CloudFormation might create IAM resources.** and click **Create**. The stack will be created in a few minutes.
8. If not already selected, select your stack by clicking on the check box to the left of your stack.
9. Click on the Events tab and refresh periodically to monitor the creation of your stack.</p>

### 2. Complete Initial Environment Configuration

In this section, you will perform configuration in the console for CloudTrail logging, CloudWatch Logs and a CloudWatch Alarm.

___Complete all the steps below unless they are marked "optional". Use arrow to expand sections marked with "(expand for details)".___

<details>
<summary><strong>1. Create a CloudTrail with the Console (expand for details)
</strong></summary><p>
<br/>

1. In the AWS Management Console, Under Management Tools, Select **CloudTrail**.

2. Click on **Trails** from the pane in left and click **Create trail** button.

3. In the **Trail name** box, type a name for your trail such as "myCloudTrail".

4. For **Apply trail to all regions?**, choose **Yes** to receive log files from all regions.

5. For **Read/Write events**, choose **All**.

6. For **Data Events**, do not select any buckets.

7. For **Create a new S3 bucket?**, choose **Yes** to create a new bucket.

8. In the **S3 bucket** field, type a name for the bucket you want to designate for log file storage such as **"myxxxxcloudtrailbucket"** substituting something unique for **xxxx**.

9. Click **Create**. The new trail will appear on the **Trails** page, which shows your trails from all regions.

Next, enable a role that CloudTrail can assume and deliver events to the log streams.
</details>
