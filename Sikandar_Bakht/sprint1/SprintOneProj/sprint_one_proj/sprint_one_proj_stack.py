from aws_cdk import (
    core as cdk,

    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam as aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_
)
from resources import constants as constants

class SprintOneProjStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.create_lambda_role()
        WH_Lambda = self.create_lambda("SikandarWebHealthLambda", "./resources/", "WH_Lambda.lambda_handler", lambda_role)
        lambda_schedule = events_.Schedule.rate(cdk.Duration.minutes(5))
        lambda_targets = targets_.LambdaFunction(handler=WH_Lambda)
        rule = events_.Rule(self, "webHealth_Invocation", description="Periodic Lambda", enabled=True, schedule=lambda_schedule, targets=[lambda_targets])
        
        #Email alert subscription
        topic = sns.Topic(self, "webHealthTopic")
        topic.add_subscription(subscriptions_.EmailSubscription(email_address = "sikandar.bakht.s@skipq.org"))
        
        #dimension for cloudwatch metrics
        dimensions = {'URL': constants.URL_TO_MONITOR}
        
        
        #Defining availability metric and alarm  
        availability_metric = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(5),
                        label = 'Availability Metric')
                        
        availability_alarm = cloudwatch_.Alarm(self, 
                        id ='Availability_Alarm',
                        metric = availability_metric,
                        comparison_operator =cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 1)
    
    
        #Defining latency metric and alarm 
        latency_metric = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_LATENCY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(1),
                        label = 'Latency Metric')
                        
        latency_alarm = cloudwatch_.Alarm(self, 
                        id ='Latency_Alarm',
                        metric = latency_metric,
                        comparison_operator =cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 0.3)
        
        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))
    
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                        ])
            
        return lambdaRole
        
        
    def create_lambda(self, id, asset, handler, role):
        ### Creates a lambda function in python3.6
        return lambda_.Function(self, 
        id,
        handler=handler,  # optional, defaults to 'handler'
        runtime=lambda_.Runtime.PYTHON_3_6,
        code=lambda_.Code.from_asset(asset),
        role=role)
    