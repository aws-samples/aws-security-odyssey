![](./images/media/image1.png){width="3.3in" height="1.43125in"}

Training and

Certification

**Monitoring Security Groups with**

**AWS Config**

Self-Paced Lab

© 2016 Amazon Web Services, Inc. and its affiliates. All rights
reserved. This work may not be reproduced or redistributed, in whole or
in part, without prior written permission from Amazon Web Services, Inc.
Commercial copying, lending, or selling is prohibited.

Errors or corrections? Email us at <aws-course-feedback@amazon.com>.

Other questions? Contact us at
<https://aws.amazon.com/contact-us/aws-training/>

Introduction
============

Overview
--------

In this lab you will learn how to use AWS Config Rules with an AWS
Lambda function to monitor the ingress ports associated with an EC2
security group. The Lambda function will be triggered whenever the
security group is modified. If the ingress rule configuration differs
from that which is coded in the function, the Lambda function will
revert the ingress rules back to the appropriate configuration. The
activity from the Lambda function can then be viewed through Amazon
Cloudwatch Logs. In an accompanying lab, Monitoring Security Groups with
Amazon CloudWatch Events, you will use a different set of services to
monitor security groups. These two labs demonstrate techniques that can
be used to provide additional layers of protection to infrastructure
assets.

Topics covered
--------------

By the end of this lab, you will be able to:

-   Upload a preconfigured Lambda function

-   Enable AWS Config

-   Create and enable a custom AWS Config rule

-   Use CloudWatch Logs to review the execution of the AWS Config rule

Technical knowledge and prerequisites
-------------------------------------

To successfully complete this lab, you should be familiar with EC2
security groups. Python programming skills are helpful, although full
solution code is provided. It would be helpful to have taken the
Introduction to AWS Lambda lab at qwiklabs.com.

Other AWS services
------------------

AWS services other than those needed for this lab are disabled by IAM
policy during your access time in this lab. In addition, the
capabilities of the services used in this lab are limited to what’s
required by the lab and in some cases are even further limited as an
intentional aspect of the lab design. Expect errors when accessing other
services or performing actions beyond those provided in this lab guide.

Using commands, scripts, or code in these labs
----------------------------------------------

Copying text from Word documents or PDF files frequently introduces line
breaks or extra (sometimes hidden) characters when you paste the text
elsewhere. For example, lab instructions sometimes fail because a
student has pasted directly from a PDF into an SSH session, and the
commands weren’t executed properly. Although we encourage students to
type many of the commands themselves to help encourage learning of the
core concepts, many labs include a text file that contains the required
commands on the qwikLABS lab overview page. This text file contains
commands required for the lab so you can easily copy and paste the
commands into the appropriate places during the lab. If you use this
text file, download it to your computer, open it in a text editor, and
read the instructions located at the beginning of the text file.

AWS Config
==========

What is AWS Config?
-------------------

AWS Config provides a detailed view of the configuration of AWS
resources in your AWS account. This includes how the resources are
related to one another and how they were configured in the past so that
you can see how the configurations and relationships change over time.
With AWS Config, you can do the following:

-   Evaluate your AWS resource configurations for desired settings.

-   Get a snapshot of the current configurations of the supported
    resources that are associated with your AWS account.

-   Retrieve configurations of one or more resources that exist in your
    account.

-   Retrieve historical configurations of one or more resources.

-   Receive a notification whenever a resource is created, modified, or
    deleted.

-   View relationships between resources. For example, you might want to
    find all resources that use a particular security group.

In this lab, we will be setting up a custom rule using a Lambda function
that is triggered whenever changes are made to a security group to
determine whether the ingress permissions differ from a preconfigured
pattern.

For further information about using AWS Config, see the official Amazon
Web Services documentation at
<https://aws.amazon.com/documentation/config/>. For pricing details, see
<https://aws.amazon.com/config/pricing/>.

What is AWS Lambda?
-------------------

Lambda is a compute service that provides resizable compute capacity in
the cloud to make web-scale computing easier for developers. You can
upload your code to AWS Lambda and the service can run the code on your
behalf using AWS infrastructure. AWS Lambda supports multiple coding
languages: Node.js, Java, or Python.

After you upload your code and create a Lambda function, AWS Lambda
takes care of provisioning and managing the servers that you use to run
the code. In this lab, you will use AWS Lambda as a trigger-driven
compute service where AWS Lambda runs your code in response to changes
to an Amazon EC2 security group. The code for the Lambda function will
be provided in an S3 bucket.

For further information about using AWS Lambda, see the official Amazon
Web Services documentation at
<https://aws.amazon.com/documentation/lambda/>. For pricing details, see
<https://aws.amazon.com/lambda/pricing/>.

What is Amazon CloudWatch Logs?
-------------------------------

You can use Amazon CloudWatch Logs to monitor, store, and access your
log files from Amazon Elastic Compute Cloud (Amazon EC2) instances, AWS
CloudTrail, and other sources. You can then retrieve the associated log
data from CloudWatch Logs.

For further information about using Amazon CloudWatch Logs, see the
official Amazon Web Services documentation at
<https://aws.amazon.com/documentation/cloudwatch/>. For pricing details,
see <https://aws.amazon.com/cloudwatch/pricing/>.

The AWS Console
===============

Accessing the AWS Management Console
------------------------------------

1.  On the Lab Details tab (in the same row of tabs as this instruction
    document), notice the lab properties:

![](./images/media/image3.png){width="1.5347222222222223in"
height="0.7222222222222222in"}

a.  **Setup Time** – The estimated time to set up the lab environment.

b.  **Duration** – The estimated time the lab should take to complete.

c.  **Access** – The time the lab will run before automatically shutting
    down.

<!-- -->

1.  Click the Start Lab button to launch the lab.

![](./images/media/image4.emf){width="1.2847222222222223in"
height="0.4583333333333333in"}

A status bar shows the progress of the lab environment creation process
(the AWS Management Console is accessible during lab resource creation,
but your AWS resources may not be fully available until the process is
complete).

1.  The **Connection** drop-down panel is automatically opened when the
    lab starts. Practice closing and re-opening it with its drop-down
    triangle. While open it may obscure some of these lab instructions
    temporarily. On the open **Connection** panel, click **Open
    Console**, which will automatically log you in to the AWS Console.
    When you return back to these instructions, close the Connection
    drop-down to resume reading and following the rest of these lab
    instructions.

![](./images/media/image5.emf){width="1.3263888888888888in"
height="0.3888888888888889in"}

Verifying Your Region in the AWS Management Console
===================================================

With Amazon EC2, you can place instances in multiple locations. Amazon
EC2 locations are composed of regions that contain Availability Zones.
Regions are dispersed and located in separate geographic areas (US, EU,
etc.). Availability Zones are distinct locations within a region that
are engineered to be isolated from failures in other Availability Zones
and to provide inexpensive, low-latency network connectivity to other
Availability Zones in the same region.

By launching instances in separate regions, you can design your
application to be closer to specific customers or to meet legal or other
requirements. By launching instances in separate Availability Zones, you
can protect your applications from localized regional failures.

Verify your region
------------------

**Tip** The AWS region name is always listed in the upper-right corner
of the AWS Management Console, in the navigation bar.

1.  Make a note of the AWS region name, for example, US West (Oregon),
    that your lab is configured for. The AWS region was set for your lab
    on the qwikLABS launch page.

2.  Use the chart below to determine the region code. You will normally
    use the code (us-west-2) instead of the region name (US West
    (Oregon)) whenever your lab asks you to specify your region.

  **Region Name**                      **Region Code**
  ------------------------------------ -----------------
  US East (Northern Virginia) Region   us-east-1
  US West (Oregon) Region              us-west-2
  Asia Pacific (Singapore) Region      ap-southeast-1
  Asia Pacific (Sydney) Region         ap-southeast-2
  Asia Pacific (Tokyo) Region          ap-northeast-1
  Asia Pacific (Seoul) Region          ap-northeast-2
  EU (Ireland) Region                  eu-west-1
  EU (Frankfurt) Region                eu-central-1

> For more information about regions, see
> <http://docs.aws.amazon.com/general/latest/gr/rande.html>.

Monitoring Security Groups with AWS Config
==========================================

Enable AWS Config
-----------------

1.  On the **Services** menu, click **Config**.

2.  Click **Get Started** if you see a button with that text.

3.  Under Resources types to record, uncheck the box **Record all
    resources supported in this region**.

4.  Click inside of the **Specific types** box. A scrollbox field will
    appear. Scroll down to the EC2 section and click **SecurityGroup**.
    You should see **EC2: Security Group** appear in the **Specific
    types** box. Hit the **Esc** (Escape) key or click outside of the
    box to close the scrollbox field.

5.  Under **Amazon S3 bucket**, select **Create a bucket**. In the
    **Bucket name** field, use the default name that is provided. Leave
    the **Prefix (optional)** window empty.

6.  Under **Amazon SNS topic**, uncheck the box **Stream configuration
    changes and notifications to an Amazon SNS topic**. We won’t be
    using SNS in the lab but if you wanted to receive an e-mail
    notifications from AWS Config, you would create an SNS topic and
    subscribe an email address to the SNS topic.

7.  Under **AWS Config Role**, select **Create a Role**. In the **Role
    name** field, use the default name that is provided.

8.  Click the **Next** button at the bottom right of the web page.

9.  On the **AWS Config Rules** page, do not select any rules. You will
    add a custom rule later. Click **Next**.

10. On the **Review** page, click **Confirm.** You will see a message
    appear saying that AWS Config is being set up. After a while, you
    will the **Resource inventory** page appear.

11. Under **Resource inventory**, click the **Resources** button. A
    scrollable window will appear with a list of check boxes. Select
    (check) all of them (be sure to scroll the entire window down as
    some may be hidden). Make sure you select (check) **SecurityGroup.**
    Click **Look Up**. You will see a message telling you that resources
    are being loaded.\
    \
    Notice that many resources appear in addition to **EC2 Security
    Group** even though we told AWS Config in step 9 to record the
    resource type **EC2 Security Group**. The reason for this is that
    AWS Config also tracks resources *related to* the resource we are
    primarily interested in because those related resources can affect
    the behavior of the primary resources, in this case EC2 security
    groups, which are being tracked. Many of these related resources are
    part of the lab environment in which you are working. We are now
    going to configure the settings of the default security group that
    has already been installed for you.

Modify the EC2 Security Group
-----------------------------

1.  Click the **Services** menu and select **VPC.** The **VPC
    Dashboard** will appear.

2.  On the left hand side of the window click **Security Groups**.

3.  There should be one security group entry with the same **sg-**
    followed by some characters. Click on the check box. You will see
    the security group configuration appear below with four “folder
    tabs.” To the right of those four tabs, you will see three square
    boxes with different levels of black and white. These will expand
    and contract the security configuration window. Click the right box
    (with the largest amount of white) to expand the window.

4.  Click on the Inbound Rules tab and click the **Edit** button.

5.  Click in the field under **Type** column and change the type to
    **HTTP (80)**. Under the **Source** column, click in the field and
    enter **0.0.0.0/0** and then click the **Add another rule** button.

6.  Click in the field under **Type** column for the new row and change
    the type to **HTTPS (443)**. Under the **Source** column, click in
    the field and enter **0.0.0.0/0** and then click the **Add another
    rule** button.

7.  Click in the field under **Type** column for the new row and change
    the type to **SMTPS (465)**. Under the **Source** column, click in
    the field and enter **0.0.0.0/0** and then click the **Add another
    rule** button.

8.  Click in the field under **Type** column for the new row and change
    the type to **IMAPS (993)**. Under the **Source** column, click in
    the field and enter **0.0.0.0/0** and click the **Save** button.

> Your Inbound Rules should look like this:
>
> ![](./images/media/image6.png){width="4.15in" height="1.95in"}
>
> You have now set up the ingress configuration of the default security
> group.

Create and Run the AWS Config Rule
----------------------------------

1.  Click on the **Services** menu and select **Config.** The AWS Config
    page will appear.

2.  On the left side of the window, click **Rules**. On the bottom of
    the window, you should see **No rules. Click Add rule to create a
    rule**. Go ahead and click the **Add rule** button. The **Add rule**
    page will appear.

3.  Click the **Add custom rule** button.

4.  In the **Name** field, enter **EC2SecurityGroup** (with underscores
    between the words).

5.  In the Description field enter Restrict ingress ports to HTTP and
    HTTPS.

6.  Click the **Create AWS Lambda function** link. This will bring up an
    additional browser window that will display **Select blueprint.**
    You will not need a blueprint. Scroll to the bottom of the screen
    and click the **Skip** button. The **Configure triggers** page will
    appear. You will not configure a trigger here so click **Next**. The
    **Configure function** page will appear.

7.  In the Name field enter awsconfig\_lambda\_security\_group

8.  In the Description field enter restrict ingress ports

9.  For Runtime select Python 2.7

10. For Code entry type select Upload a file from Amazon S3

11. In the **S3 link URL** field enter

> [**https://s3-us-west-2.amazonaws.com/labmonitorsecuritygroups/awsconfig\_lambda\_security\_group.zip**](https://s3-us-west-2.amazonaws.com/labmonitorsecuritygroups/awsconfig_lambda_security_group.zip)

1.  In the Handler field enter
    **awsconfig\_lambda\_security\_group.lambda\_handler**

2.  In the **Role** field select **Create a custom role** and a new page
    window will appear.

3.  In the Role Name field enter
    awsconfig\_lambda\_ec2\_security\_group\_role

4.  Click on **View Policy Document** to open the policy window and then
    click on the **Edit** link. Click **Ok** if a warning message
    appears about reading the documentation.

5.  In the policy window erase the existing content and enter the
    following:

> {
>
> "Version": "2012-10-17",
>
> "Statement": \[
>
> {
>
> "Effect": "Allow",
>
> "Action": \[
>
> "logs:CreateLogGroup",
>
> "logs:CreateLogStream",
>
> "logs:PutLogEvents"
>
> \],
>
> "Resource": "arn:aws:logs:\*:\*:\*"
>
> },
>
> {
>
> "Effect": "Allow",
>
> "Action": \[
>
> "config:PutEvaluations",
>
> "ec2:DescribeSecurityGroups",
>
> "ec2:AuthorizeSecurityGroupIngress",
>
> "ec2:RevokeSecurityGroupIngress"
>
> \],
>
> "Resource": "\*"
>
> }
>
> \]
>
> }

1.  Click the **Allow** button. The page will close and you will return
    to the Lambda **Configure function** page.

2.  Let the **Memory (MB)** field remain with the default value of 128.

3.  In the **Timeout** fields, set **min** to 1 and **sec** to 0. Lambda
    functions can run for a maximum of five minutes. This is particular
    function typically takes less than five seconds to run so allowing
    one minute should be more than adequate.

4.  For **VPC** accept the default value of **No VPC**. Click **Next**.

5.  On the **Review** page note that the timeout value appears as 60.
    Click **Create function**. You should return to the Lambda dashboard
    and see four tabs. Click on the **Code** tab. You should see Python
    code that looks similar to what appears below. If you don’t see
    code, revisit the work you did in steps 35 and 36. The part of the
    handler name to the left of the period must match the file name.

![](./images/media/image7.png){width="7.090277777777778in"
height="3.611111111111111in"}

Let’s take a look at a few things in the code. Scroll down to where you
see the value **REQUIRED\_PERMISSIONS**.

![](./images/media/image8.png){width="6.701388888888889in"
height="4.208333333333333in"}

This is an array of desired ingress IP Permissions in the format used by
the **describe\_security\_groups()** API call which is used later in the
code. Notice that the array only contains permissions for HTTP (TCP port
80) and HTTPS (TCP port 443). It does not contain the permissions we
added for SMTPS (TCP port 465) and IMAPS (TCP port 993).

If the ingress permissions contain anything other than the permissions
in this array, the code uses the
**authorize\_security\_group\_ingress()** and
**revoke\_security\_group\_ingress()** calls to add or remove
permissions as appropriate. Therefore, we should expect that the SMTPS
(TCP port 465) and IMAPS (TCP port 993) permissions should be removed
when we run this runction.

1.  On the upper right part of the page you should some text following
    **ARN**. Copy the text beginning with **arn:aws:lambda** all the way
    to the end into scratch text file or leave it in your copy/paste
    buffer. It should look something like this:

> arn:aws:lambda:us-west-2:123456899012:function:awsconfig\_lambda\_security\_group
>
> Go back to the **AWS Config** page that should still be open to **Add
> custom rule**.\
> \
> NOTE: If you closed the AWS Config page accidentally, then go back to
> the Lambda page you were just on and click **Services** and select
> **Config** and do steps 26-29 again and then continue below.

1.  In the **AWS Lambda function ARN** field, enter the
    **arn:aws:lambda** value that you copied in the previous step.

2.  For Trigger type select **Configuration changes**.

3.  For **Scope of changes** select **Resources**. A **Resources**
    selection scrollbox will appear.

4.  Pick **SecurityGroup**. You do leave **Resource identifier** empty
    since we only have one security group in this lab.

5.  In the **Key** field enter **debug** and in the **Value** field
    enter **true** to generate additional data you can look at later if
    you choose.

6.  Click **Save**. You will return to the AWS Config Rules page. Under
    the **Compliance** column, you will see the function has been
    submitted for an initial evaluation. This initial evaluation may
    take several minutes to complete. This same evaluation will also
    take place whenever the security group is changed again in the
    future. Click the refresh button periodically as well to update the
    evaluation status.

> ![](./images/media/image9.png){width="0.5208333333333334in"
> height="0.4583333333333333in"}

1.  Once the compliance evaluation has taken place, you should see the
    following:

![](./images/media/image10.png){width="6.548611111111111in"
height="0.8680555555555556in"}

Revisiting the VPC Security Group
---------------------------------

1.  We will now examine the VPC security group that we had previously
    created to allow HTTP, HTTPS, IMAPS, and SMTPS traffic. Click the
    **Services** menu and select **VPC**. The **VPC Dashboard** will
    appear.

2.  On the left hand side of the window click Security Groups.

3.  Click the **Inbound** tab that appears below. Notice that only HTTP
    and HTTPS traffic are permitted as shown below.

![](./images/media/image11.png){width="5.416666666666667in"
height="1.9513888888888888in"}

This corresponds to the **REQUIRED\_PERMISSIONS** that were configured
into the Lambda function as described in step 44. The Lambda function
detected the additional permissions for SMTPS (TCP port 465) and IMAPS
(TCP port 993) that were present in the security group and removed them.
In this case, the detection happened during the initial rule validation.
If you were to modify the security group again, a compliance evaluation
would be triggered which would again invoke the Lambda function and the
changes would be reverted.

\
Using Amazon CloudWatch Logs for Verification
---------------------------------------------

1.  We will now use Amazon CloudWatch Logs to see what the Lambda
    function did. Click the **Services** menu and select **Cloudwatch.\
    **

2.  On the left side of page, select **Logs**.

3.  Click on the link that contains
    **awsconfig\_lambda\_security\_group**.

4.  Under **Log Streams**, beginning with the top link, click each link
    until you see an entry that contains the words **revoking for** and
    expand the entry. You should see something similar to this. The
    security group values have been blacked out. This shows that the two
    entries for ports 993 and 465 have been removed.

![](./images/media/image12.png){width="7.097222222222222in"
height="0.9652777777777778in"}

1.  (Optional) If the lab timer shows you have another 15 minutes
    remaining, modify the ingress ports of the security group as
    described in steps 17-24. That will trigger another evaluation of
    the security group configuration. After 8-13 minutes, the ingress
    port configuration will revert to include only HTTP (TCP port 80)
    and HTTPS (TCP port 443). You will be able to verify this by
    revisiting the security group settings.

[]{#_Toc460861014 .anchor}**End Your Lab**

Follow these steps to close the console, end your lab, and evaluate the
experience.

1.  In the upper right of the navigation bar of the AWS Management
    Console, click **&lt;yourqwiklabsacct@yourmail.com&gt; @
    &lt;AccountNumber&gt;**, and then click **Sign Out**.

2.  On the qwikLABS page, click **End Lab**.

3.  In the confirmation message, click **OK**.

4.  (Optional) Select the applicable number of stars, type a comment,
    and then click **Submit**.

> Note: The number of stars indicates the following:

-   1 star = Very dissatisfied

-   2 stars = Dissatisfied

-   3 stars = Neutral

-   4 stars = Satisfied

-   5 stars = Very satisfied

> You may close the dialog if you don’t want to provide feedback.

Conclusion
==========

Congratulations! You have now successfully:

-   Enabled AWS Config

-   Uploaded a Lambda function to support a rule for AWS Config that
    evaluations permissions on an EC2 security group.

-   Modified the default VPC Security group to contain both compliant
    and noncompliant permissions

-   Enabled the AWS Config Rule and observed the results

-   Examined the activity of the Lambda function using Amazon Cloudwatch
    Logs.

Additional resources
====================

For more information about AWS Lambda and Amazon CloudWatch, see:

-   More Self-Paced Labs can be found at <https://qwiklabs.com>

-   For more information about AWS Config, see
    <https://aws.amazon.com/config/>

-   For more information about AWS Lambda, see
    <https://aws.amazon.com/lambda/>

-   For more information about Amazon CloudWatch, see
    <https://aws.amazon.com/cloudwatch/>

-   For more information on AWS Training & Certification, see
    <http://aws.amazon.com/training/>

For feedback, suggestions, or corrections, please email us at
<aws-course-feedback@amazon.com>.
