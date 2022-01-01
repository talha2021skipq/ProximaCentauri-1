def lambda_handler(event, context):
    return 'Helloo {},{}!'.format(event['first_name'], event['last_name'])
