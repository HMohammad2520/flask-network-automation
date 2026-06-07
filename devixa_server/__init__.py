import uuid
import traceback
import importlib
import importlib.util
from pathlib import Path
from flask import Flask, Blueprint, json
from flask_sqlalchemy import SQLAlchemy
from typing import List
from .__version__ import get_version
from .config import cnf
from .views import blueprints, apps_bp
from .models import db


def create_app(name: str) -> Flask:
    app = Flask(
        name,
        static_folder='application/static',
        template_folder='application/templates',
    )
    app.secret_key = cnf.flask_secret
    app.config['SQLALCHEMY_DATABASE_URI'] = cnf.connection_string

    return app


def add_error_handler(app: Flask) -> Flask:
    @app.errorhandler(Exception)
    def base_error_handler(exp: Exception):
        # TODO: Make first and last error code in CNF
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

            # TODO: Add path to cnf
            with open(f'.log/err_{timed_uuid}.json', 'w') as error_file:
                error_file.write(
                    json.dumps(data, indent=4),
                )

        raise exp
    return app


def register_extentions(apps_bp: Blueprint, apps_dir: Path | str = 'extentions') -> List[Blueprint]:
    apps_path = Path(apps_dir)

    if not apps_path.exists():
        raise RuntimeError('Extentions Folder Should exist.')

    blueprints = []
    # Iterate through each subfolder in apps directory
    for app_folder in apps_path.iterdir():
        if not app_folder.is_dir():
            continue

        # Check for __init__.py file
        init_file = app_folder / '__init__.py'
        if not init_file.exists():
            continue

        # Dynamic import of the app module
        module_name = f"external_apps_{app_folder.name}"
        spec = importlib.util.spec_from_file_location(module_name, init_file)
        if not spec:
            continue

        module = importlib.util.module_from_spec(spec)

        if not spec.loader:
            continue

        spec.loader.exec_module(module)

        extention_bp = getattr(
            module, 'blueprint', getattr(
                module, 'bp', None
                )
            )

        # Config and Register the blueprint
        if extention_bp:
            extention_bp.static_folder = str(app_folder / 'static')
            extention_bp.template_folder = str(app_folder / 'templates')
            extention_bp.url_prefix = str('/' + extention_bp.name)

            apps_bp.register_blueprint(extention_bp)
            blueprints.append(extention_bp)
            print(
                f"Registered blueprint: apps{extention_bp.url_prefix}"
            )

        else:
            print(
                f"No 'bp' or 'blueprint' attribute found in {app_folder.name}"
            )

    return blueprints


def register_bluprints(app: Flask, bluprints: list[Blueprint]) -> Flask:
    for blueprint in bluprints:
        if not blueprint.name == 'root':
            blueprint.url_prefix = '/' + blueprint.name

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
    'register_extentions',
    'register_bluprints',
    'blueprints',
    'apps_bp',
    'cnf',
    'db',
]
