from flask import jsonify


def init_app(app):
    """
    handle errors when we use abort() method by giving response code
    eg: see auth.py (abort function called by giving response codes)
    """

    @app.errorhandler(404)
    def not_found(e):
        data = {'status': 404, 'message': 'Not Found'}
        res = jsonify(data)
        return res

    @app.errorhandler(400)
    def bad_request(e):
        data = {'status': 400, 'message': 'Bad Request'}
        res = jsonify(data)
        return res
