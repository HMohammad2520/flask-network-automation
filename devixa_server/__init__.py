import uuid
import traceback
import importlib
import importlib.util
from pathlib import Path
from flask import Flask, Blueprint, redirect, url_for, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from typing import Type, List
from .__version__ import get_version
from .config import cnf
from .views import blueprints, apps_bp
from .models import db, User


def create_app(name: str) -> Flask:
    app = Flask(
        name,
        static_folder='devixa_server/static',
        template_folder='devixa_server/templates',
    )
    app.secret_key = cnf.flask_secret
    app.config['SQLALCHEMY_DATABASE_URI'] = cnf.connection_string

    return app


def init_database(app: Flask, db: SQLAlchemy) -> Flask:
    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


def init_user_management(app: Flask, User: Type[User]) -> Flask:
    login_manager = LoginManager(app)

    def user_loader(id):
        return User.query.get(id)

    login_manager.user_loader(user_loader)

    def unauthuraized():
        return redirect(url_for('auth.login'))

    login_manager.unauthorized_handler(unauthuraized)

    return app


def init_admin_user(app: Flask, User: Type[User]) -> Flask:
    with app.app_context():
        admin_user = User.query.filter(User.username == 'admin').first()
        if admin_user is None:
            password = input('Admin Password:')
            re_password = input('Retype Password:')
            if password == re_password:
                admin_user = User.create(
                    username='admin', password=password, email='admin@example.com'
                )

    return app


def register_extentions(apps_bp: Blueprint, apps_dir: Path | str = 'extensions') -> List[Blueprint]:
    apps_path = Path(apps_dir)

    if not apps_path.exists():
        raise RuntimeError('Extensions Folder Should exist.')

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
