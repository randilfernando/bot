import requests

from wit.exceptions import APIException

config = {}
params = {}
headers = {}


builtin_intents = {
    'greetings': 'greet',
    'thanks': 'thank',
    'bye': 'exit'
}


def init(c):
    global config, headers, params

    config = c

    params = {
        'v': config['version']
    }

    headers = {
        'Authorization': 'Bearer %s' % config['token']
    }


def get_intents():
    response = requests.get('https://api.wit.ai/entities/intent',
                            params=params,
                            headers=headers)

    if response.status_code != 200:
        raise APIException

    return response.json()['values']


def add_intent(value):
    response = requests.post('https://api.wit.ai/entities/intent/values',
                             params=params,
                             headers=headers,
                             json={
                                 'value': value
                             })

    if response.status_code != 200:
        raise APIException


def add_expression(value, expression):
    response = requests.post('https://api.wit.ai/entities/intent/values/%s/expressions' % value,
                             params=params,
                             headers=headers,
                             json={
                                 'expression': expression
                             })

    if response.status_code != 200:
        raise APIException


def remove_expression(value, expression):
    response = requests.delete('https://api.wit.ai/entities/intent/values/%s/expressions/%s' % (value, expression),
                               params=params,
                               headers=headers)

    if response.status_code != 200:
        raise APIException


def get_message_intent(question):
    p = {
        'v': params['v'],
        'q': question
    }
    response = requests.get('https://api.wit.ai/message',
                               params=p,
                               headers=headers)

    if response.status_code != 200:
        raise APIException

    data = response.json()

    intent = {
        'value': 'unidentified',
        'confidence': 0
    }

    for key, value in data['entities'].items():
        if value[0]['confidence'] > intent['confidence']:
            if key == 'intent':
                intent['value'] = value[0]['value']
                intent['confidence'] = value[0]['confidence']
            elif value[0]['value'] == 'true' and key in builtin_intents.keys():
                intent['value'] = builtin_intents[key]
                intent['confidence'] = value[0]['confidence']

    return intent


