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


        #####################################################################################################################
        ##                                 WebHealth Monitor Lambda Configuration                                          ##
        #####################################################################################################################
        
        lambda_role = self.create_lambda_role()
        WH_Lambda = self.create_lambda("SikandarWebHealthLambda", "./resources/", "WH_Lambda.lambda_handler", lambda_role)
        lambda_schedule = events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_targets = targets_.LambdaFunction(handler=WH_Lambda)
        rule = events_.Rule(self, "webHealth_Invocation", description="Periodic Lambda", enabled=True, schedule=lambda_schedule, targets=[lambda_targets])
        
        
        #####################################################################################################################
        ##                              Setting Up DynamoDB WebHealth Logging Table                                        ##
        #####################################################################################################################
        
        db_table = self.create_db_table(id = "SprintOneTable", table_Name = "MonitorDB", part_key=db.Attribute(name="Timestamp", type=db.AttributeType.STRING))
        db_lambda_role = self.create_db_lambda_role()
        DB_Lambda = self.create_lambda("SikandarDBLambda", "./resources/", "DB_Lambda.lambda_handler", db_lambda_role)
        db_table.grant_full_access(DB_Lambda)
        
        #####################################################################################################################
        ##                      Setting Up SNS Notifications for Email and Lambda Triggering                               ##
        #####################################################################################################################

        topic = sns.Topic(self, "webHealthTopic")
        topic.add_subscription(subscriptions_.EmailSubscription(email_address = "sikandar.bakht.s@skipq.org"))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn = DB_Lambda))
        
        #####################################################################################################################
        ##                                 Retrieving Custom URLs from S3 Bucket                                           ##
        #####################################################################################################################
        
        URLS_MONITORED = sb('sikandarbakhtskipq').load('urls_dict.json')
        K=list(URLS_MONITORED['URLS'][0].keys())
        
        #####################################################################################################################
        ##                                 Creating Cloudwatch Metrics and Alarms For URL 1                                ##
        #####################################################################################################################
        
        dimensions = {'URL': URLS_MONITORED['URLS'][0][K[0]]}
        
        #AVAILABILITY METRIC AND ALARM
        
        availability_metric_0 = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(5),
                        label = f'{K[0]} Availability Metric')
                        
        availability_alarm_0 = cloudwatch_.Alarm(self, 
                        id = f'Sikandar Bakht_{K[0]}_Availability_Alarm',
                        alarm_description = f"Alarm to monitor availability of {K[0]}",
                        alarm_name = f'{K[0]} Availability Alarm',
                        metric = availability_metric_0,
                        comparison_operator =cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 1)
    
    
        #LATENCY METRIC AND ALARM
        
        latency_metric_0 = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_LATENCY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(1),
                        label = f'{K[0]} Latency Metric')
                        
        latency_alarm_0 = cloudwatch_.Alarm(self, 
                        id = f'Sikandar Bakht_{K[0]}_Latency_Alarm',
                        alarm_description = f"Alarm to monitor latency of {K[0]}",
                        alarm_name = f'{K[0]} Latency Alarm',
                        metric = latency_metric_0,
                        comparison_operator =cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 0.27)
        
        availability_alarm_0.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm_0.add_alarm_action(actions_.SnsAction(topic))
        
        #####################################################################################################################
        ##                                 Creating Cloudwatch Metrics and Alarms For URL 2                                ##
        #####################################################################################################################
        dimensions = {'URL': URLS_MONITORED['URLS'][0][K[1]]}
        
        #AVAILABILITY METRIC AND ALARM
        
        availability_metric_1 = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(5),
                        label = f'{K[1]} Availability Metric')
                        
        availability_alarm_1 = cloudwatch_.Alarm(self, 
                        id = f'Sikandar Bakht_{K[1]}_Availability_Alarm',
                        alarm_description = f"Alarm to monitor availability of {K[1]}",
                        alarm_name = f'{K[1]} Availability Alarm',
                        metric = availability_metric_1,
                        comparison_operator =cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 1)
    
    
        #LATENCY METRIC AND ALARM
        
        latency_metric_1 = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_LATENCY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(1),
                        label = f'{K[1]} Latency Metric')
                        
        latency_alarm_1 = cloudwatch_.Alarm(self, 
                        id = f'Sikandar Bakht_{K[1]}_Latency_Alarm',
                        alarm_description = f"Alarm to monitor latency of {K[1]}",
                        alarm_name = f'{K[1]} Latency Alarm',
                        metric = latency_metric_1,
                        comparison_operator =cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 0.22)
        
        availability_alarm_1.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm_1.add_alarm_action(actions_.SnsAction(topic))
        
        #####################################################################################################################
        ##                                 Creating Cloudwatch Metrics and Alarms For URL 3                                ##
        #####################################################################################################################
         
        dimensions = {'URL': URLS_MONITORED['URLS'][0][K[2]]}
        
        #AVAILABILITY METRIC AND ALARM
        
        availability_metric_2 = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(5),
                        label = f'{K[2]} Availability Metric')
                        
        availability_alarm_2 = cloudwatch_.Alarm(self, 
                        id = f'Sikandar Bakht_{K[2]}_Availability_Alarm',
                        alarm_description = f"Alarm to monitor availability of {K[2]}",
                        alarm_name = f'{K[2]} Availability Alarm',
                        metric = availability_metric_2,
                        comparison_operator =cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 1)
    
    
        #LATENCY METRIC AND ALARM
        
        latency_metric_2 = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_LATENCY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(1),
                        label = f'{K[2]} Latency Metric')
                        
        latency_alarm_2 = cloudwatch_.Alarm(self, 
                        id = f'Sikandar Bakht_{K[2]}_Latency_Alarm',
                        alarm_description = f"Alarm to monitor latency of {K[2]}",
                        alarm_name = f'{K[2]} Latency Alarm',
                        metric = latency_metric_2,
                        comparison_operator =cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 0.2)
        
        availability_alarm_2.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm_2.add_alarm_action(actions_.SnsAction(topic))
        
        
         #####################################################################################################################
        ##                                 Creating Cloudwatch Metrics and Alarms For URL 4                                ##
        #####################################################################################################################
        dimensions = {'URL': URLS_MONITORED['URLS'][0][K[3]]}
        
        #AVAILABILITY METRIC AND ALARM
        
        availability_metric_3 = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(5),
                        label = f'{K[3]} Availability Metric')
                        
        availability_alarm_3 = cloudwatch_.Alarm(self, 
                        id = f'Sikandar Bakht_{K[3]}_Availability_Alarm',
                        alarm_description = f"Alarm to monitor availability of {K[3]}",
                        alarm_name = f'{K[3]} Availability Alarm',
                        metric = availability_metric_3,
                        comparison_operator =cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 1)
    
    
        #LATENCY METRIC AND ALARM
        
        latency_metric_3 = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_LATENCY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(1),
                        label = f'{K[3]} Latency Metric')
                        
        latency_alarm_3 = cloudwatch_.Alarm(self, 
                        id = f'Sikandar Bakht_{K[3]}_Latency_Alarm',
                        alarm_description = f"Alarm to monitor latency of {K[3]}",
                        alarm_name = f'{K[3]} Latency Alarm',
                        metric = latency_metric_3,
                        comparison_operator =cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                        datapoints_to_alarm = 1,
                        evaluation_periods = 1,
                        threshold = 0.8)
        
        availability_alarm_3.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm_3.add_alarm_action(actions_.SnsAction(topic))
     
        #####################################################################################################################
        ##                                           Class Method Definitions                                              ##
        #####################################################################################################################
        
        
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
                        ])
            
        return lambdaRole
    
    def create_db_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role-db",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
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
 