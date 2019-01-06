from bot.db import get_db
from bot.exceptions import IntentNotAvailable
from wit import client
from wit.exceptions import APIException

intents = {}
threshold = 0.5


def init_app(app):
    global threshold, client_config

    threshold = app.config['INTENT_THRESHOLD']

    client_config = {
        'version': app.config['WIT_VERSION'],
        'token': app.config['WIT_TOKEN']
    }


def init_bot():
    global intents, threshold

    intents = {}

    client.init(client_config)

    for value in client.get_intents():
        intents[value['value']] = value['expressions']

    db_intents = get_db().execute('SELECT intent FROM responses').fetchall()

    for db_intent in db_intents:
        if db_intent['intent'] not in intents.keys():
            intents[db_intent['intent']] = []
            client.add_intent(db_intent['intent'])


def teach_expression(intent, expression):
    try:
        if intent not in intents.keys():
            client.add_intent(intent)
            intents[intent] = []

        client.add_expression(intent, expression)
        intents[intent].append(expression)
    except APIException:
        raise APIException


def teach_response(intent, response):
    entry = get_db().execute('SELECT id FROM responses WHERE intent = ?', (
        intent,
    )).fetchone()

    if entry is not None:
        get_db().execute('UPDATE responses SET response = ? WHERE intent = ?', (
            response,
            intent
        ))
    else:
        get_db().execute('INSERT INTO responses(intent, response) VALUES (?, ?)', (
            intent,
            response,
        ))
        get_db().commit()

    if intent not in intents.keys():
        intents[intent] = []
        client.add_intent(intent)


def ask_question(question, suggestions = 'enabled'):
    intent = client.get_message_intent(question)

    if intent['value'] != 'unidentified' and \
            suggestions == 'enabled' and \
            intent['confidence'] < threshold:
        return {
            'type': 'suggestion',
            'suggestions': intents[intent['value']]
        }
    else:
        entry = get_db().execute('SELECT response FROM responses WHERE intent = ?', (
            intent['value'],
        )).fetchone()

        if entry is not None and entry['response'] != '':
            return {
                'type': 'answer',
                'intent': intent['value'],
                'response': entry['response']
            }
        else:
            return {
                'type': 'answer',
                'intent': intent['value'],
            }


def get_intents():
    return {
        'intents': list(intents.keys())
    }


def get_intent(intent):
    if intent not in intents.keys():
        raise IntentNotAvailable

    data = {
        'intent': intent,
        'expressions': [],
        'response': ''
    }

    if intent in intents.keys():
        data['expressions'] = intents[intent]

    entry = get_db().execute('SELECT response FROM responses WHERE intent = ?', (
        intent,
    )).fetchone()

    if entry is not None:
        data['response'] = entry['response']

    return data
