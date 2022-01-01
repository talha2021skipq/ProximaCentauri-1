

# Sprint1: Creation of web health monitoring system
## Project Summary 

In the sprint1 at skipq, we designed a web health monitoring system, that will periodically monitor the web health metrics like latency and availability and
then raise an alarm when the metrics breach the specified threshold. The rasied alarms will be stored in a dynamodb  table.

## Services Covered

1. AWS Dynamodb
2. AWS Cloudwatch
3. S3 buckets
4. AWS lambda
5. AWS SNS
6. AWS events
7. AWS events target

## Installation Guide

Follow these easy steps to set up the environment ro run the project:

1. Install requirements.txt file using pip install
2. Do `cdk init --language python` to setup python projet
3. make sure that there are 7 python files in resources folder nd  python files in project subfolder
3. In the project directory, perform cdk synth and then cdk deploy
3. Make sure that there are 7 python files in resources folder nd  python files in project subfolder.

## Author

Talha Naeem... talha.naeem.s@skipq.org


This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
~





