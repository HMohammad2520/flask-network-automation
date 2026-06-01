import uuid
import traceback
from flask import Flask, Blueprint, json
from flask_sqlalchemy import SQLAlchemy
from .__version__ import get_version
from .config import cnf
from .views import blueprints
from .models import db


def create_app(name: str) -> Flask:
    app = Flask(name)
    app.secret_key = cnf.flask_secret
    app.config['SQLALCHEMY_DATABASE_URI'] = cnf.connection_string

    return app

def add_error_handler(app: Flask) -> Flask:
    @app.errorhandler(Exception)
    def base_error_handler(exp: Exception):
        ## TODO: Make first and last error code in CNF
        code = getattr(exp, 'code', 500)
        if 400 < code <= 500:
            timed_uuid = uuid.uuid7()
            setattr(exp, 'uuid', timed_uuid)

            data = {
                'uuid': str(timed_uuid),
                'time': timed_uuid.time,
                'code': code,
                'name': getattr(exp, 'name', 'Unkhown Error') or exp.__class__.__name__,
                'description': getattr(exp, 'description', 'No more details'),
                'traceback': '\n'.join(traceback.format_exception(exp)),
            }

            ## TODO: Add path to cnf
            with open(f'.log/err_{timed_uuid}.json', 'w') as error_file:
                error_file.write(
                    json.dumps(data, indent=4),
                )

        raise exp
    return app


def register_bluprints(app: Flask, bluprints: list[Blueprint]) -> Flask:
    for blueprint in bluprints:
        app.register_blueprint(blueprint)

    return app


def init_database(app: Flask, db: SQLAlchemy) -> Flask:
    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


__all__ = [
    'get_version',
    'create_app',
    'register_bluprints',
    'blueprints',
    'cnf',
    'db',
]
