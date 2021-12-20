from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as event_,
    aws_events_targets as targets_,
    aws_cloudwatch as cloudwatch_,
    aws_iam,
    aws_sns as sns,
    aws_sns_subscriptions as subsribe,
    aws_cloudwatch_actions as cw_actions
#    aws_dynamodb as db
)
#from aws_cdk import aws_cloudwatch_actions as actions_
from resources import constants as constant_

class IrfanSkipQProject1Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #creating dynamodb 
        #dynamodb = self.create_table()
                
        lambda_role = self.create_lambda_role()
        hi_lamda = self.create_lambda('heloHellammbda',"./resources",'lambda.lambda_handler',lambda_role)
        hello_lamda = self.create_lambda('FirstHellammbda',"./resources",'Monitor_webhealth.lambda_handler',lambda_role)
        dynamo_lamda = self.create_lambda('dynamodbHellammbda',"./resources",'dynamodb_lambda.lambda_handler',lambda_role)
        #reading s3 bucket using lambda
        s3bucket_lamda = self.create_lambda('s3bucket_lambda',"./resources",'s3bucket_read.lambda_handler',lambda_role)
        
        lambda_schedule = event_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler = hello_lamda)
        our_rule = event_.Rule(self, id = "MonitorwebHealth",enabled = True, schedule= lambda_schedule,targets =[lambda_target])
        sns_topic = sns.Topic(self, 'WebHealth')
        sns_topic.add_subscription(subsribe.EmailSubscription("muhammad.irfan.hassan.s@skipq.org"))
        #sns_topic.add_subscription(subsribe.LambdaSubscription(fn = dynamo_lamda)
        
        Dimensions={'URL': constant_.URL}

        availabilty_metric=cloudwatch_.Metric(namespace=constant_.URL_NameSpace, 
                    metric_name=constant_.URL_Aailibilty, 
                    dimensions_map=Dimensions,
                    period=cdk.Duration.minutes(1),
                    label='availabilty_metric'
                    )

        availabilty_Alarm=cloudwatch_.Alarm(self, 
                    id ="AvailabiltyAlarm",
                    metric = availabilty_metric,
                    comparison_operator = cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                    datapoints_to_alarm=1,
                    evaluation_periods=1,
                    threshold =1
                    )

                    
        latency_metric=cloudwatch_.Metric(namespace=constant_.URL_NameSpace, 
                    metric_name=constant_.URL_Latency, 
                    dimensions_map=Dimensions,
                    period=cdk.Duration.minutes(1),
                    label='latency_metric'
                    )

        
        latency_Alarm=cloudwatch_.Alarm(self, id="latencyAlarm",
                    metric = latency_metric,
                    comparison_operator = cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                    datapoints_to_alarm=1,
                    evaluation_periods=1,
                    threshold = 0.35
                    )
        
        availabilty_Alarm.add_alarm_action(cw_actions.SnsAction(sns_topic))
        latency_Alarm.add_alarm_action(cw_actions.SnsAction(sns_topic))

    def create_lambda_role(self):
        lambda_role = aws_iam.Role(self, "lambda-role", 
        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies = [
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSlambdaBasicExecutionRole'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess')
            ]
        )
        return lambda_role
  
        
    
    def create_lambda(self,id, asset, handler,role):
        return lambda_.Function(self, id,
        code = lambda_.Code.from_asset(asset),
        handler=handler,
        runtime= lambda_.Runtime.PYTHON_3_6,
        role=role
        )
        
#    def create_table(id_,region_,table_name_,):
#        boto3.resources(id_, region_name = region_)
#        table = dynamodb.create_table(
#                TableName = table_name_,
#                KeySchema =[
#                    {
#                    
#                }
#                ]
#        )
    