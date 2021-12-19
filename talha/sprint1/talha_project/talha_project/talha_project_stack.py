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
    aws_s3 as s3_, 
    aws_sqs as sqs_,
    aws_s3_notifications as s3n_,
    aws_dynamodb as db_,
  #  aws_lambda_event_sources as lambda_events_,
    
)

from resources import constants as constants

class TalhaProjectStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lambda_role=self.create_lambda_role()
    # The code that defines your stack goes here
        HWlambda=self.create_lambda('FirstHWlambda', './resources','webHealth_talha_lambda.lambda_handler' ,lambda_role)
        Talha_db_lambda=self.create_lambda('neTwlambda', './resources','talha_dynamoDb_lambda.lambda_handler' ,lambda_role)
 
    #Creating an event after every one minute
        lambda_schedule= events_.Schedule.rate(cdk.Duration.minutes(1))
    #Setting target to our New WH lambda for the event##
        lambda_target= targets_.LambdaFunction(handler=HWlambda)
    #defining rule for lambda function invokation event
        rule=events_.Rule(self, "WebHealth_Invokation",
            description="Periodic Lambda",enabled=True,
            schedule= lambda_schedule,
            targets=[lambda_target])
        #create table in dynamo db
        try:
            dynamo_table= self.create_table()
        except: pass
        #give read write permissions to our lambda
        dynamo_table.grant_read_write_data(Talha_db_lambda)
        ###defining SNS service    
        topic = sns.Topic(self, "TalhaSkipQWebHealthTopic")
        #sns subscription with email
    #    topic.add_subscription( subscriptions_.EmailSubscription('talha.naeem.s@skipq.org'))
        #topic = sns.Topic(self, "TalhaSkipQdynamodbTopic") # NO NEED TO define another TOPIC within one stack
        #topic.add_subscription(subscriptions_.LambdaSubscription(fn=))
###Add lambda subscription to db_lambda, whenever an event occurs at the specified topic
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=Talha_db_lambda))
     
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
            threshold=0.49 #constants.THRESHOLD_LATENCY
            )
    #link sns and sns subscription to alarm
        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))
    #creating s3bucket 
        bucket_talha= s3_.Bucket(self, "talha_first_bucket")
    #create a queue that will get bucket events
        queue = sqs_.Queue(self, 'QueueForTalha_bucket',
        visibility_timeout=cdk.Duration.seconds(300) ) 
        # Now, create an event on bucket that will work with sqs queue
        bucket_talha.add_event_notification( s3_.EventType.OBJECT_CREATED, s3n_.SqsDestination(queue) )
        #event permission
#        event_put_policy = aws_iam.PolicyStatement(
 #           effect= aws_iam.Effect.ALLOW, resources=['*'], actions=['events:PutEvents'])
  #      task_definition.add_to_task_role_policy(event_put_policy)
            # S3 Object (bucket_name and key are identifiers)
        #GET s3://talhaprojectstack-talhafirstbucket65240409-xd9dx9unwvol/urls_list.txt
        '''s3 = boto3.client('s3')
        result = s3.list_objects(Bucket = "talha_first_bucket", Prefix='/something/')
        for o in result.get('Contents'):
            data = s3.get_object(Bucket="talha_first_bucket", Key=o.get('Key'))
            contents = data['Body'].read()
            print(contents.decode("utf-8"))'''
##Define Event for dynamoDB to be called, and the event is when the alarm is up
        #db_lambda_schedule= events_.Schedule.rate(cdk.Duration.minutes(1))
    #Setting target to our New WH lambda for the event##
        #db_lambda_target= targets_.LambdaFunction(handler=db_lambda)
    #defining rule for lambda function invokation event
        #db_rule=events_.Rule(self, "Alarm_to_db", description="Add alarms to dynamoTable",enabled=True,
        #    schedule= db_lambda_schedule,
         #   targets=[db_lambda_target])
            
#When alarm is published on sns topic, it will invoke the db_lmbda with the alarm message as payload
        #dead_letter_queue = sqs_.Queue(self, "deadLetterQueue")
     # #  Talha_db_lambda.add_event_source(lambda_events_.SnsEventSource(topic))
            #filter_policy={},
            #dead_letter_queue=dead_letter_queue)) 
        #dblambda_target= targets_.LambdaFunction(handler=Talha_db_lambda)
    #defining rule for lambda function invokation event
        #rule=events_.Rule(self, "db_Invokation",
         #   description="Db writerLambda",enabled=True,
          #  schedule= lambda_schedule,
           # targets=[dblambda_target]) 
            
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
    def create_table( self):
        return db_.Table(self,id="Table", table_name="TalhaAlarmTable",partition_key=db_.Attribute(name="id", type=db_.AttributeType.STRING), 
            sort_key=db_.Attribute(name="createdDate", type=db_.AttributeType.STRING))
        