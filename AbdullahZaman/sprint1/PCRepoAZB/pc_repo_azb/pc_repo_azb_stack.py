from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_
)
from resources import constants as constants

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class PcRepoAzbStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        lambda_role = self.create_lambda_role()
        hw_lambda = self.create_lambda("FirstHWLambda", "./resources", "webhealth_lambda.lambda_handler", lambda_role)
        # We define the schedule, target and the rule for our lambda
        
        lambda_schedule = events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler=hw_lambda)
        rule = events_.Rule(self, "WebHealth_Invocation", description = "Periodic Lambda", 
                            enabled=True, schedule=lambda_schedule, targets=[lambda_target])
        
        topic = sns.Topic(self, "WebHealthTopic")
        topic.add_subscription(subscriptions_.EmailSubscription("abdullah.zaman.babar.s@skipq.org"))
        
        #subscriptions_.EmailSubscription("abdullah.zaman.babar.s@skipq.org")
        
        dimension = {"URL" : constants.URL_TO_MONITOR}
        availability_metric = cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,
                                            metric_name=constants.URL_MONITOR_NAME_Availability, 
                                            dimensions_map=dimension, 
                                            period=cdk.Duration.minutes(1), label="Availability Metric")
        availability_alarm = cloudwatch_.Alarm(self, id="AvailabilityAlarm",
                                        metric=availability_metric,
                                        comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                                        datapoints_to_alarm=1,
                                        evaluation_periods=1,
                                        threshold=1)
                                        
        dimension = {"URL" : constants.URL_TO_MONITOR}
        latency_metric = cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,
                                            metric_name=constants.URL_MONITOR_NAME_Latency, 
                                            dimensions_map=dimension, 
                                            period=cdk.Duration.minutes(1), label="Latency Metric")
        latency_alarm = cloudwatch_.Alarm(self, id="LatencyAlarm",
                                        metric=latency_metric,
                                        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                        datapoints_to_alarm=1,
                                        evaluation_periods=1,
                                        threshold=0.28)
    
        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))
    
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
            assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                ])
        return lambdaRole
    
    def create_lambda(self, newid, asset, handler, role):
         return lambda_.Function(self, id = newid,
 			                    runtime = lambda_.Runtime.PYTHON_3_6,
			                    handler = handler,
			                    code = lambda_.Code.asset(asset),
			                    role=role,
			                    )
