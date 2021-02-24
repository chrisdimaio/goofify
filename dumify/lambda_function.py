import json
import logging
import os
import urllib.parse
import urllib3

from base64 import b64decode
from random import randint


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info(json.dumps(event))

    r = postmessage(getdata(event))

    logger.info(json.dumps(
        {
            'postmessage_response': {
                'status': r.status,
                'data': str(r.data)
            }
        }
    ))
    return {
        'statusCode': 200,
        'body': ''
    }


def dumify(dumstring):
    dumified = ""
    for c in dumstring:
        if randint(0, 1) == 1:
            dumified += c.upper()
        else:
            dumified += c.lower()
    return dumified


def postmessage(data):
    token = os.environ['bearer_token']

    http = urllib3.PoolManager()
    r = http.request(
        'POST',
        'https://slack.com/api/chat.postMessage',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        body=json.dumps({
            'as_user': 'true',
            'channel': data['channel_id'],
            'username': data['user_name'],
            'text': dumify(data['text']),
        })
    )
    return r


def getdata(event):
    body = event['body']
    raw_data = urllib.parse.unquote_plus(str(b64decode(body).decode('utf-8')))
    data = {}
    pieces = raw_data.split("&")
    for piece in pieces:
        k, v = piece.split("=")
        data[k] = v
    return data
