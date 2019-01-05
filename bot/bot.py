from flask import (
    Blueprint,
    jsonify,
    request,
    abort
)

from engine.engine import teach_response, ask_question, teach_expression, get_intent, get_intents
from engine.exceptions import IntentNotAvailable
from wit.exceptions import APIException

bp = Blueprint('bot', __name__, url_prefix='/bot')


@bp.route('/teach-expression', methods=['POST'])
def te():
    data = request.json

    if 'intent' not in data or 'expression' not in data:
        abort(400)
        return

    try:
        teach_expression(data['intent'], data['expression'])
        return jsonify({'status': 'success'})
    except APIException:
        abort(400)


@bp.route('/ask-question', methods=['POST'])
def aq():
    data = request.json

    if 'question' not in data:
        abort(400)
        return

    if 'mode' not in data or data['mode'] not in ['suggest', 'force']:
        data['mode'] = 'suggest'

    return jsonify(ask_question(data['question'], data['mode']))


@bp.route('/teach-response', methods=['POST'])
def tr():
    data = request.json

    if 'intent' not in data or 'response' not in data:
        abort(400)
        return

    teach_response(data['intent'], data['response'])
    return jsonify({'status': 'success'})


@bp.route('/intents', methods=['GET'])
def gis():
    return jsonify(get_intents())


@bp.route('/intents/<intent>', methods=['GET'])
def gi(intent):
    try:
        return jsonify(get_intent(intent))
    except IntentNotAvailable:
        abort(404)
