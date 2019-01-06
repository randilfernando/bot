import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the bot
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'bot.sqlite'),
        WIT_VERSION='20170307',
        INTENT_THRESHOLD=0.5
    )

    app.config.from_pyfile('config.py', silent=True)

    try:
        app.config.from_mapping(
            WIT_TOKEN=os.environ['WIT_TOKEN']
        )
    except KeyError:
        pass

    if test_config is not None:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    # bind db object with newly created flask application
    db.init_app(app)

    from . import error_handler
    # bind error handler with newly created flask application
    error_handler.init_app(app)

    from . import api
    # bind api with newly created flask application
    app.register_blueprint(api.bp)

    from . import engine
    # bind engine with newly created flask application
    engine.init_app(app)
    # initialize engine

    with app.app_context():
        engine.init_bot()

    return app
