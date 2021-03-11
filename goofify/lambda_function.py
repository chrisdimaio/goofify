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


def dumify(string):
    if len(string) >= 3:
        words = list(string)

        # Always make the first letter lowercase
        words[0] = words[0].lower()

        # the second uppercase
        words[1] = words[1].upper()

        # the last uppercase
        words[-1] = words[-1].upper()

        # and the second to last lowercase
        words[-2] = words[-2].lower()

        # then randomly flip the ones in between.
        words[2:-2] = [l.upper() if randint(0, 1) else l for l in words[2:-2]]

        return ''.join(words)
    return string


"""
    Experimental method to detect dumified strings.
"""


def isdumified(string):
    print(string)
    words = list(string)

    if len(words) < 3:
        return False
    if (
        (words[0].isalpha() & words[0].isupper()) &
        (words[1].isalpha() & words[1].islower()) &
        (words[-1].isalpha() & words[-1].islower()) &
        (words[-2].isalpha() & words[-2].isupper())
    ):
        return False

    uppers = len(
        [l for l in filter(lambda n: n.isupper() & n.isalpha(), words[2:-2])])

    # Calculate the ratio of uppercase letters to lowercase.
    ratio = uppers/len([l for l in filter(lambda n: n.isalpha(), words)])

    # Got these thresholds by calculating a million ratios of dumified strings.
    if ratio < .20 or ratio > .82:
        return False
    return True


def getdata(event):
    body = event['body']
    raw_data = urllib.parse.unquote_plus(str(b64decode(body).decode('utf-8')))
    data = {}
    pieces = raw_data.split("&")
    for piece in pieces:
        k, v = piece.split("=")
        data[k] = v
    return data


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
