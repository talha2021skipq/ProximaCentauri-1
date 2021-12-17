from aws_cdk import (
    core as cdk,
    aws_lambda as _lambda,
    aws_events as events_,
    aws_events_targets as targets_,# aws_sqs as sqs,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_s3 as s3_
)
from resources import constants as constants
class TalhaProjectStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lambda_role=self.create_lambda_role()
    # The code that defines your stack goes here
        HWlambda=self.create_lambda('FirstHWlambda', './resources','webHealth_talha_lambda.lambda_handler' ,lambda_role)
        #db_lambda=self.create_lambda('DynamoDBlambda','/resources','dynamoDb_lambda.handler',lambda_role)
    #Creating an event after every one minute
        lambda_schedule= events_.Schedule.rate(cdk.Duration.minutes(1))
    #Setting target to our New WH lambda for the event
        lambda_target= targets_.LambdaFunction(handler=HWlambda)
    #defining rule for lambda function invokation event
        rule=events_.Rule(self, "WebHealth_Invokation",
            description="Periodic Lambda",enabled=True,
            schedule= lambda_schedule,
            targets=[lambda_target])
        ###defining SNS service    
        topic = sns.Topic(self, "TalhaSkipQWebHealthTopic")
        #sns subscription with email
        topic.add_subscription( subscriptions_.EmailSubscription('talha.naeem.s@skipq.org'))
        #topic.add_subscription(subscriptions_.LambdaSubscription(fn=))

        dimension=    {   'URL':  constants.URL_TO_MONITOR}
    #create cloudwatch metric for availability 
        availability_metric=cloudwatch_.Metric( namespace= constants.URL_MONITOR_NAMESPACE,metric_name=constants.URL_MONITOR_NAME1A,
            dimensions_map=dimension, period=cdk.Duration.minutes(1), label='Avaiability_metric')
    #setting an alarm for availability
        availability_alarm= cloudwatch_.Alarm(self,
            id='Availability_alarm', metric=availability_metric,
            comparison_operator= cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD, 
            datapoints_to_alarm=1,
            evaluation_periods=1, 
            threshold= 1#constants.THRESHOLD_AVAIL
            )
    #create a metric class for latency
        latency_metric=cloudwatch_.Metric(namespace= constants.URL_MONITOR_NAMESPACE, metric_name=constants.URL_MONITOR_NAME1L, 
            dimensions_map=dimension, period=cdk.Duration.minutes(1),label='Latency_metric')
    #create an alarm for latency
        latency_alarm= cloudwatch_.Alarm(self,
            id='Latency_alarm', metric=latency_metric,
            comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            datapoints_to_alarm=1,
            evaluation_periods=1,  
            threshold=0.48 #constants.THRESHOLD_LATENCY
            )
    #link sns and sns subscription to alarm
        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))
    ###############################Worked for me without lambdarole, because I am root user
    def create_lambda_role(self):
        lambdaRole=aws_iam.Role(self,"lambda-role",
        assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess')
            ]) 
        return lambdaRole##

    def create_lambda( self,id,asset,handler, role):#
        return _lambda.Function(self, id,
        code=_lambda.Code.from_asset(asset),
        handler=handler,
        runtime=_lambda.Runtime.PYTHON_3_6,
        role=role
        )
        # example resource
        # queue = sqs.Queue(
        #     self, "TalhaProjectQueue",
        #     visibility_timeout=cdk.Duration.seconds(300),
        # )
