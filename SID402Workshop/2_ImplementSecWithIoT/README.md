# 2017 AWS re:INVENT - SID402 - Lab 2

**Implementing Security Controls in the World of Internet, Big Data,**  
**IoT, E-Commerce, and Open Communications Platforms**

**Implementing Security with AWS IoT**

Self-Paced Lab

&copy; 2017 Amazon Web Services, Inc. and its affiliates. All rights reserved. This work may not be reproduced or redistributed, in whole or in part, without prior written permission from Amazon Web Services, Inc. Commercial copying, lending, or selling is prohibited.

Errors or corrections? Email us at <aws-course-feedback@amazon.com>.

Other questions? Contact us at <https://aws.amazon.com/contact-us/aws-training/>

# Introduction

## Overview

In this lab, you will set up an environment using the AWS IoT (Internet of Things) service. You will create a simulated device (a &ldquo;thing&rdquo;) and connect it to the AWS IoT service and watch traffic flow between the device and AWS IoT. You will then enhance the security of the communication between the device and AWS IoT and, in so doing, learn more about the various security features offered by the service.

*NOTE: Going forward, we will use the terms &ldquo;device&rdquo; and &ldquo;thing&rdquo; interchangeably.*

## Topics covered

By the end of this lab, you will be able to:

* Create a test AWS IoT environment using AWS CloudFormation. The environment will contain an Amazon EC2 instance running a package named [Node-RED](https://en.wikipedia.org/wiki/Node-RED). Node-RED provides a web-based interface that allows you to create message &ldquo;flows&rdquo; (i.e. sequences of transmissions). Node-RED can send these message flows using the MQTT and TLS protocols, which are used by AWS IoT. In short, Node-RED lets you simulate an AWS IoT device (a &ldquo;thing&rdquo;).

* Configure Node-RED to simuilate AWS IoT device (a &ldquo;thing&rdquo;) and then test communication with the AWS IoT service.

* Adjust the security permissions within AWS IoT to more tightly restrict the communication to AWS IoT.

## Prerequisites

This lab assumes the following:

* You have a general knowledge of AWS services including the use of the AWS Console, AWS CloudFormation, AWS IAM, Amazon EC2, and Amazon VPC.

* You have an AWS account and an IAM user with full administrative privileges. If you do not have full administrative privileges, you will need to have at a minimum the ability to:

  * Create and manage AWS CloudFormation stacks

  * Create and manage Amazon VPC and related components

  * Create and manage Amazon EC2 t2 instances and associate Elastic IP addresses

  * Create and manage IAM groups and roles

  * Fully manage AWS IoT

* Only one person will be doing this lab in a specific AWS account in a given region. If more than one person is using the same AWS account for this lab at the same time, each must use a different AWS IoT region or make adjustments to the templates.

# Overview of Key Services Used in this Lab

## AWS IoT

AWS IoT is a managed cloud platform that lets connected devices easily and securely interact with cloud applications and other devices. AWS IoT can support billions of devices and trillions of messages, and can process and route those messages to AWS endpoints and to other devices reliably and securely.

## AWS CloudFormation

AWS CloudFormation gives developers and systems administrators an easy way to create and manage a collection of related AWS resources, provisioning and updating them in an orderly and predictable fashion.

# Select a Region

AWS IoT is located in many [regions](http://docs.aws.amazon.com/general/latest/gr/rande.html#iot_region) across the world. We will provide shortcuts for the us-east-1, us-east-2, and us-west-2 regions in this document and ask that you choose one of these three regions for the lab. As noted above, if more than one person is doing the lab in the same AWS account, each person should use a different region.


# Initial sign in

1. Sign in to the AWS management console at: <https://console.aws.amazon.com/console/home>

# Build the Node-RED Environment

Our labs will use AWS CloudFormation to provision a web-based environment with Node-RED. Node-RED allows you to simulate an IoT device including the sending and receiving of IoT messages using the MQTT protocol. The AWS CloudFormation template will create a complete environment consisting of an Amazon VPC and an Amazon EC2 instance on which Node-RED will be installed.

2. Click the link below corresponding to the region in which you wish to deploy the lab environment.

    [N. Virginia (us-east-1)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=IoTSecurityLab&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/scripts/IoT_Security_Lab_Connect_VPC.yaml)

    [Ohio (us-east-2)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=IoTSecurityLab&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/scripts/IoT_Security_Lab_Connect_VPC.yaml)

    [Oregon (us-west-2)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=IoTSecurityLab&templateURL=https://s3-us-west-2.amazonaws.com/sid402-artifacts/scripts/IoT_Security_Lab_Connect_VPC.yaml)

3. A new browser tab or page will appear with the CloudFormation template selected. Click on **Next** to start populating the fields listed below.

    **Stack Name**: The name for the CloudFormation stack. The default name is IoTSecurityLab,

    **Allowed IP Range**: The IP address range that can browse to the Amazon EC2 instance running Node-RED. The default is 0.0.0.0/0 which is any IPv4 address on the Internet. For this short duration lab, this is fine. For something running longer term, you would want to restrict this to a safe IP range.

    **Instance Type**: The size of Amazon EC2 instance to deploy for Node-RED. The default is t2.micro and is fine for this lab.

    Click on **Next**.

4. On the next page, you can create tags to be applied to resources, then click **Next**.

5. Review the settings. When requested, click the check box to acknowledge that IAM resources may be created and then click **Create**. You will return to the CloudFormation console. The process will take five to seven minutes to complete. While the stack is building, proceed to the next page to create your first AWS IoT device (a &ldquo;thing&rdquo;).

# Define Device

    You will now define an IoT device. A device is recognized by AWS IoT through a certificate. You will create a certificate and attach it to the device. You will also attach a policy to the device that gives the device (&ldquo;thing&rdquo;) full access to AWS IoT. Later in this lab, you will configure the Node-RED with this certificate which will cause AWS IoT to recognize Node-RED as an AWS IoT device.

6. Make sure you are still working in the same AWS region in which you are building the AWS CloudFormation stack.

7. Select the service **AWS IoT** from the AWS Console. If you see a **Get started** button, click that.

8. From the menu on the left, select **Registry** &gt; **Things** and the click the **Register a thing** button (if there are already things listed, click the **Create** button instead).

9. Enter the name `device1` and click **Create thing**. You should see a new entry as shown below.

    ![](images/image2.png "image")

10. On the left select **Security &gt; Certificates**, then click **Create a certificate** and then Click **Create certificate.** You will then be presented with a page telling you the certificate has been created and given the opportunity to download four items as shown below. Continue below this picture for download instructions.

    ![](images/image3.png "image")

    Use the top three download links to download the certificate, public key, and private key to a folder on your system. Also download the root CA from the link above the Activate button by right-clicking and saving the file as **rootCA.pem**. Once done and verified you have the files locally save, click **Activate** and then scroll to the bottom of the window and click **Attach a policy**.

    You have thus far created a device and a certificate. You will now define what the holder of the certificate (which will eventually be Node-RED running on Amazon EC2) can do.

11.  Clock Create new policy.

12.  On the **Create a policy** page create the statement as follows:

    ![](images/image4.png "image")

    **Name**: device1\_full\_access

    **Action**: iot:\*

    **Resource**: ARN: \*

    **Effect**: Allow

    This represents a policy named device1\_full\_access that can perform all iot actions (iot:\*) on all resources. In other words, the policy will grant full IoT access to any certificate to which the policy is attached.

13.  Select **Create**.

14.  From the main AWS IoT menu, select **Security Certificates.**

15.  Select the certificate that you created above by hovering over the certificate and checking the blue box that appears. With it checked, select the drop-down menu **Actions** and click on **Attach policy**. Then select the **device1\_full\_access** policy and click **Attach**. You have now attached the policy to the certificate.

16.  Select the drop-down menu **Actions** and click on **Attach thing** and select the thing named **device1**. Click **Attach**. You have now attached the certificate with its policy to the device. Later in this lab, you will configure Node-RED with the certificate that has this policy causing, Node-RED to be recognized by AWS IoT as **device1**.

17.  On this AWS IoT console home page, near the bottom left click Settings. Copy the value in the **Endpoint** field and save it in a text file. You will need this value later in the lab when you configure Node-RED.

# Configure Node-RED

18.  By this point, the CloudFormation stack with the Node-RED Amazon EC2 instance should be complete Go to the AWS CloudFormation console, select the stack and look at the output tab. You should see the following values:

    **HostIPAddress**: The IP address of the EC2 instance

    **NodeREDURL**: The URL of the EC2 instance

19.  Browse to the URL and you should see Node-RED appear.

    ![](images/image5.png "image")

    The interface has three sections. Going from left to right:

    **Nodes**: These represent actions or objects for Node-RED.

    **Flow Canvas**: You position nodes, configure them, and connect them on the canvas to create message flows.

    **Info/Debug**: The info tab will provide more details on the selected node. The debug tab will show in real time all activity for the debug nodes.

    Click on the **device1** tab. This will display the two flows to be tested. The first flow, **Publish time locally**, generate a binary timestamp (the Generate Timestamp node), then have that converted to a friendly date and time (the timestampToString node), and then finally print the time to the debug window (the Print Time node). The second flow will do something similar, except you will see there is an additional output to be configured to send the message to the AWS IoT service.

    **First flow - Publish time locally**

20.  On the right side of the make sure the debug tab is selected.

21.  On the Generate Timestamp node for Publish time locally, click the button on the left side. This will generate the timestamp, then convert and send. You will see the message in the debug frame. Every click on the inject node (Generate Timestamp) will publish a message in the debug window. See the vertical red arrows below for clarification.

    ![](images/image6.png "image")

    **Second flow - Single click message to AWS IoT**

22.  The second flow under **Single click message to AWS IoT** does two things. Like the first flow, Node-RED will print a timestamp locally. Additionally, there is also a branch flow which translates the time to JSON format (the timestampToJSON node) and then sends the message to AWS IoT (the AWS IoT node). You will see a red alert icon on the upper right corner of the AWS IoT node because some configuration information is missing.

    To configure the AWS IoT node, double-click it. This will bring up a window that allows you to edit the MQTT properties of the node. [MQTT](https://en.wikipedia.org/wiki/MQTT) is one of the underlying network protocols used by AWS IoT. Click the pencil icon as shown below by the red arrow.

    ![](images/image7.png "image")

    Another window will appear on which you will enter MQTT configuration information.

    On the Connection tab, configure the following:

    **Server**: Endpoint value that you copied earlier
    **Port**: 8883
    **Client ID**: device1

    Now check the box named Enable Secure SSL/TLS communication. The window should like similar to that shown below.

    ![](images/image8.png "image")

23.  Click the pencil next to the Add new tls-config dropdown as shown by the red arrow above. A new window will appear as shown below.

    ![](images/image9.png "image")

24.  On the Add new-tls-config screen, make sure the **Use key and certificates from local files** is deselected (which would cause Node-RED to use files on the Node-RED instance itself), and instead select the Upload button for each and navigate to the directory where the files are saved. The files will have names similar to the following:

    **Certificate**: c1234567-certificate.pem

    **Private Key**: c1234567-private.pem.key

    **CA Certificate**: rootCA.pem

    **Verify server certificate**: selected

    **Name**: IoT Security Lab

25.  Then click **Add**, which will bring you back to the **Add mqtt-broker config node** window.

26.  From the mqtt-broker config node page, click **Add**. You will return to the **Edit mqtt out node** window.

27.  Enter the following information into the fields in the window.

    **Topic:** topic1

    **QoS**: 0

    **Name:** AWS IoT

    The server name will already be filled in based on the information you have provided as shown in the screen below. Later in the lab, we will show how to subscribe to messages sent to **topic1** to verify communication from AWS IoT and Node-RED.

    ![](images/image10.png "image")

28.  Click **Done** to go back to the main GUI.

29.  Finally, notice that the **Deploy** icon in the upper right of the GUI is red. This means changes have been made and need to be deployed. Click on this button and the flow will be saved, validated, and ready for use. If validation succeeds, the AWS IoT node (the Node-RED Amazon EC2 instance) will connect to the AWS IoT platform. You should see a green icon with &ldquo;connected&rdquo; under the AWS IoT node, Node-RED was able to successfully connect to the AWS IoT platform.

30.  Bring up the AWS Console in a new browser window or tab and navigate to the AWS IoT console and select **Test**. Then select Subscribe to a topic link, enter **topic1** as the topic, and finally click the Subscribe to topic button per the figure below.

    ![](images/image11.png "image")

    The MQTT client will then appear as shown below.

    ![](images/image12.png "image")

31.  Return to the Node-RED window. Clean out the debug window by clicking the trash can icon. Click the button to the left of the Generate Timestamp node for the Single click message to AWS IoT flow. You will see the friendly date and time posted in the debug window, but you will also see the message published in the MQTT client in the AWS Console. Notice also that the AWS IoT node continues to show that it is connected which means that the policy attached to the certificate does allow the desired communication.

    ![](images/image13.png "image")

32.  Now return to the AWS IoT window with the MQTT client. You should see a message that was published to topic1 as shown in the figure below.

    ![](images/image14.png "image")

    You have now done the following:

    * Defined an IoT device.

    * Created a certificate and attached a policy which has full access to AWS IoT

    * Launched a Node-RED instance on AWS and configured Node-RED with the certificate information from AWS IoT, thereby enabling the Node-RED instance to simulate an IoT device and communicate with AWS IoT

    * Captured traffic from Node-RED within AWS IoT.

    You will now learn how to restrict access to AWS IoT.

# Restricting Access to AWS IoT

## Create Permissions for Device Specific Topics

Earlier in this lab you created a policy for your AWS IoT certificate that was very open and allowed the holder of that certificate to publish to any IoT topic. We are now going to show you how to restrict that policy so it only allows publishing to the topic we have already created.

33.  Go to the main IoT console and choose **Security &gt; Policies**. You should see a policy named device1\_full\_acccess. Click directly on the policy name.

    On the top of the window you will see the policy ARN (Amazon Resource Name). It will look something like:

    `arn:aws:iot:us-west-2:123456789012:policy/device1_full_access`

    Copy the region name (`us-west-2` in the above example) and the account number (`123456789012` in the above example) to a scratch file for future use.

34.  Go back to the main IoT console and choose **Security &gt; Policies**. Click **Create**.

    Enter `device1_allow_publish` and click **Advanced mode.**

34.  Replace the JSON with the content below, replacing `REGION` and `ACCOUNT` with the values you copied earlier. Make sure you retain all of the colon (&ldquo;:&rdquo;) separators.

    ```
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "iot:Subscribe",
            "iot:Connect",
            "iot:Receive"
          ],
          "Resource": [
            "*"
          ]
        },
        {
          "Effect": "Allow",
          "Action": [
            "iot:Publish"
          ],
          "Resource": [
            "arn:aws:iot:REGION:ACCOUNT:topic/topic1"
          ]
        }
      ]
    }

    ```

    Click **Create**.

35.  Navigate to **Security-&gt;Certificates** and select your certificate then click on **Policies**. Now select **Attach policy** under Actions and select **device1\_allow\_publish**. Then detach the **device1\_full\_access** policy from the certificate.

36.  Go to the IoT console and select **Test**. Subscribe to **topic1**.

37.  Go to the Node-RED window and generate another message under **Single click message to AWS IoT**. You should see messages continue to appear on the test window. The AWS IoT node should continue to remain connected.
    You have now restricted the AWS IoT device represented by Node-RED so that it can only publish to the topic named **topic1**.

38.  On the Node-RED window, double click on the **AWS IoT** node. Change the topic name to **topic2**. Click **Done**. Click **Deploy**.

39.  Generate another message under **Single click message to AWS IoT**. You should see the AWS IoT node disconnect for a few seconds as shown in the figure below. This is because you are only allowed to publish to topic **topic1**.

    ![](images/image15.png "image")

# Conclusion

Congratulations! You have now successfully:

-   Configured a device in AWS IoT

-   Launched an Amazon EC2 instance with the Node-RED platform

-   Associated Node-Red with the IoT device by attaching a certificate

-   Captured traffic from Node-RED with AWS IoT

-   Configured AWS IoT security policies to restrict actions from IoT devices

# Clean Up Lab

To clean up the lab environment, follow the remaining steps.

1.  Delete the AWS CloudFormation stack you previously launched.

2.  Remove all IOT configuration items (things, certificates, policies).
