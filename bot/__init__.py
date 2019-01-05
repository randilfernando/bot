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

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from database import db
    # bind db object with newly created flask application
    db.init_app(app)

    from . import error_handler
    # bind error handler with newly created flask application
    error_handler.init_app(app)

    from . import bot
    # bind api with newly created flask application
    app.register_blueprint(bot.bp)

    from engine import engine
    # bind engine with newly created flask application
    engine.init_app(app)
    # initialize engine

    with app.app_context():
        engine.init_engine()

    return app
