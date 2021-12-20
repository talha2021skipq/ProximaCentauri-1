#!/usr/bin/env python3
import os
import json
import aws_cdk.core as cdk
from resources.S3bucket import S3Bucket as sb
from sprint_one_proj.sprint_one_proj_stack import SprintOneProjStack

sb_url = sb('sikandarbakhtskipq')
URLS_TO_MONITOR = {'URLS':[{'Skipq':"www.skipq.org", 'Twitch':"www.twitch.tv", 'Python':"www.python.org", 'NUST':"nust.edu.pk"}]}

sb_url.dump('urls_dict.json', URLS_TO_MONITOR)

app = cdk.App()
SprintOneProjStack(app, "SprintOneProjStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
