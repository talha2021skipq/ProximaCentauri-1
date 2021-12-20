from aws_cdk import (
    core as cdk,

    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam as aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as db
)
from resources import constants as constants
from resources.S3bucket import S3Bucket as sb
import json 
class SprintOneProjStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.create_lambda_role()
        WH_Lambda = self.create_lambda("SikandarWebHealthLambda", "./resources/", "WH_Lambda.lambda_handler", lambda_role)
        lambda_schedule = events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_targets = targets_.LambdaFunction(handler=WH_Lambda)
        rule = events_.Rule(self, "webHealth_Invocation", description="Periodic Lambda", enabled=True, schedule=lambda_schedule, targets=[lambda_targets])
        
        URLS_MONITORED = sb('sikandarbakhtskipq').load('urls_dict.json')
        dict_keys=list(URLS_MONITORED['URLS'][0].keys())
        
        db_table = self.create_db_table(id = "SprintOneTable", table_Name = "MonitorDB", part_key=db.Attribute(name="Timestamp", type=db.AttributeType.STRING))
        db_lambda_role = self.create_db_lambda_role()
        
        DB_Lambda = self.create_lambda("SikandarDBLambda", "./resources/", "DB_Lambda.lambda_handler", db_lambda_role)
        db_table.grant_full_access(DB_Lambda)
        #Email alert subscription
        topic = sns.Topic(self, "webHealthTopic")
        
        topic.add_subscription(subscriptions_.EmailSubscription(email_address = "sikandar.bakht.s@skipq.org"))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn = DB_Lambda))
        #dimension for cloudwatch metrics
        
        dimensions = {'URL': URLS_MONITORED['URLS'][0][dict_keys[0]]}
        
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
        
        
        '''
        #DEFINING FOR URL 2
        dimensions = {'URL': constants.URL_TO_MONITOR[1]}
        
        availability_metric_1 = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(5),
                        label = 'Availability Metric')
                        
        availability_alarm_1 = cloudwatch_.Alarm(self, 
                        id ='Availability_Alarm', alarm_description = f"Alarm to monitor availability of {constants.URL_TO_MONITOR[1]}",
                        alarm_name = f"{constants.URL_NAME_TO_MONITOR[1]} Availability Alarm",
                        metric = availability_metric_1,
                        comparison_operator =cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 1)
    
    
        #Defining latency metric and alarm 
        latency_metric_1 = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_LATENCY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(1),
                        label = 'Latency Metric')
                        
        latency_alarm_1 = cloudwatch_.Alarm(self, 
                        id ='Latency_Alarm', alarm_description = f"Alarm to monitor latency of {constants.URL_TO_MONITOR[1]}",
                        alarm_name = f"{constants.URL_NAME_TO_MONITOR[1]} Latency Alarm",
                        metric = latency_metric_1,
                        comparison_operator =cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 0.3)
        
        availability_alarm_1.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm_1.add_alarm_action(actions_.SnsAction(topic))
        
        '''
        
    
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                        ])
            
        return lambdaRole
    
    def create_db_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role-db",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess')
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
    
    def create_db_table(self, id, table_Name, part_key):
        return db.Table(self, 
        id, 
        billing_mode=db.BillingMode.PAY_PER_REQUEST, 
        table_name=table_Name, 
        partition_key=part_key )
 