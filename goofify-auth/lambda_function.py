import json
import logging
import os
import urllib3


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info(event)

    endpoint = 'https://slack.com/api/oauth.v2.access'
    code = event['queryStringParameters']['code']
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
    redirect_uri = os.environ['redirect_uri']

    http = urllib3.PoolManager()
    r = http.request(
        'GET',
        f'{endpoint}?code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}'
    )
    logger.info(r.data)

    return {
        'statusCode': 200,
        'body': 'Success'
    }
