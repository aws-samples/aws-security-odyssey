# ___AWS Security Odyssey___

## 2017 AWS re:Invent - SID402 - Workshop
### Implementing Security Controls in the World of Internet, Big Data, IoT, E-Commerce, and Open Communications Platforms
<br/>
#### ___Welcome to the IthaCorp Cloud Engineering Team. Let the Odyssey begin!___
<company name is TBD>

IthaCorp Enterprises is a multinational conglomerate with businesses in multiple industries including manufacturing, hospitality, IoT and consumer electronics. IthaCorp provides an array of back office and public facing services to internal and external customers. To support these services, a significant AWS footprint has been established consisting of multiple workloads leveraging resources including Amazon VPC, Amazon EC2 and Amazon S3. As this footprint has grown organically, the IthaCorp Cloud Engineering Team has identified the need to enhance security controls across their AWS environments.

You have have joined the Cloud Engineering Team to lead the AWS security enhancement project. You decide to use the [Cloud Adoption Framework (CAF) - Security Perspective](https://d0.awsstatic.com/whitepapers/AWS_CAF_Security_Perspective.pdf) as a framework for the project. This entails implementing security controls across the following areas:

- **Directive controls** establish the governance, risk, and compliance models the environment will operate within.
- **Preventive controls** protect your workloads and mitigate threats and vulnerabilities.
- **Detective controls** provide full visibility and transparency over the operation of your deployments in AWS.
- **Responsive controls** drive remediation of potential deviations from your security baselines.

To help deliver the project, you will use [AWS VPC](https://aws.amazon.com/ec2/), [Amazon VPC](https://aws.amazon.com/vpc/), [Amazon S3](https://aws.amazon.com/s3/), [AWS CloudTrail](https://aws.amazon.com/cloudtrail/), [AWS CloudWatch](https://aws.amazon.com/cloudwatch/), [Amazon Lambda](https://aws.amazon.com/lambda/), [AWS IoT](https://aws.amazon.com/iot/).

### Prerequisites

### AWS Account

In order to complete this workshop you'll need an AWS Account with access to create Amazon EC2, Amazon VPC, AWS Identity and Access Management (IAM), Amazon Simple Storage Service (S3), AWS Lambda, and AWS IoT resources.

The code and instructions in this workshop assume only one student is using a given AWS account at a time. If you try sharing an account with another student, you'll run into naming conflicts for certain resources. You can work around this by either using a suffix in your resource names or using distinct Regions, but the instructions do not provide details on the changes required to make this work.

### Region

Choose an AWS Region to execute the workshops which support the complete set of services covered in the material including AWS Lambda, Amazon Kinesis Streams, Amazon Kinesis Firehose, Amazon Kinesis Analytics, and Amazon Athena. Use the [Region Table](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) to determine which services are available in a Region. Regions that support these services include **US East (N. Virginia)** and **US West (Oregon)**.

## Modules

1. [Monitoring Security Events in AWS](1_MonitoringSecEvents)
2. [Implementing Security with AWS IoT](2_ImplementSecWithIoT)
3. [Automating Security Remediation in AWS](3_AutoSecRemediation)
