def lambda_handler(event, context):
    return 'hello {} {} !'.format(event['first_name'],event['last_name'])