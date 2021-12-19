# SPINT1 : WEBHEALTH STACK
## Overview
Using AWS CDK to measure the availability and latency(delay) of a custom list of websites and monitor the results on a CloudWatch. Then setting up alarms on metrics when the prescribed thresholds are breached. Each alarm is published to SNS notifications which triggers a lambda function that writes the alarm information into DynamoDB.
![WebHealth](https://github.com/abdullah2021skipq/ProximaCentauri/blob/main/AbdullahZaman/tinker.png)
## Configuration Instructions
* Update Python and aws
* Use _aws codecommit_ to create a local repository.
* Add _ssh keys_ for authentication.
* Create a CDK project using _**cdk init --language python**_
* Install the dependencies from _requirements.txt_
## Troubleshooting Instructions
If the _**cdk synth**_ instruction doesn't create CLOUDFORMATION template in the virtual environemt, navigate to the _**.venv/bin**_ directory and execute the following:
<p align=center><span style="color:red">python3 -m pip install -r path_to_requirements.txt/requirements.txt</span></p>

