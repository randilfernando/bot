from flask import (
    Blueprint,
    jsonify,
    request,
    abort
)

from bot import engine
from bot.exceptions import IntentNotAvailable
from wit.exceptions import APIException

bp = Blueprint('bot', __name__, url_prefix='/bot')


@bp.route('/intents', methods=['GET'])
def gis():
    return jsonify(engine.get_intents())


@bp.route('/intents/<intent>', methods=['GET'])
def gi(intent):
    try:
        return jsonify(engine.get_intent(intent))
    except IntentNotAvailable:
        abort(404)


@bp.route('/intents/<intent>/responses', methods=['POST'])
def tr(intent):
    data = request.json

    if 'response' not in data:
        abort(400)
        return

    engine.teach_response(intent, data['response'])
    return jsonify({'status': 'success'})


@bp.route('/intents/<intent>/expressions', methods=['POST'])
def te(intent):
    data = request.json

    if 'expression' not in data:
        abort(400)
        return

    try:
        engine.teach_expression(intent, data['expression'])
        return jsonify({'status': 'success'})
    except APIException:
        abort(400)


@bp.route('/questions', methods=['POST'])
def aq():
    data = request.json

    if 'question' not in data:
        abort(400)
        return

    if 'suggestions' not in data or data['suggestions'] not in ['enabled', 'disabled']:
        data['suggestions'] = 'enabled'

    return jsonify(engine.ask_question(data['question'], data['suggestions']))
