from flask import Blueprint, current_app, request, abort, jsonify
from typing import Dict, Optional
from ..models import APIMethod, model_map, db
from .. import cnf

api_bp = Blueprint('api', __name__)

"""
@api.errorhandler(Exception)
def api_error_handler(exp: Exception):
    if current_app.debug:
        raise exp

    return jsonify(
    {
        'code': getattr(exp, 'code', 500),
        'error': getattr(exp, 'name', 'Unkhown Error'),
        'description': getattr(exp, 'description', "No more information provided."),
        }
    )
"""


@api_bp.before_request
def before_request():
    authorization = request.headers.get('Authorization')
    if not authorization:
        if not cnf.anonymous_mode:
            return abort(401)

        return

    token = authorization.split('bearer', 1)
    if len(token) != 2:
        return abort(403)

    token = token[1]
    # TODO: Check Token Here


@api_bp.route('/')
def index():
    return jsonify('Welcome to API')


def method_execution(
    model_name: str,
    method_name: str,
    pk: Optional[int] = None,
):
    Model = model_map.get(model_name)
    method = APIMethod.get_method(Model, method_name)
    instance = None

    if not Model or not method:
        return abort(404)

    if pk:
        instance = Model.query.get(pk)

        if not instance:
            return abort(404)

    allowed_methods = APIMethod.get_request_methods(method)
    kwargs: Dict[str, str] = {}

    if request.method not in allowed_methods:
        return abort(405)

    if request.method == 'GET':
        kwargs.update(request.args)

    elif request.method in ('POST', 'PUT', 'DELETE'):
        if request.is_json:
            kwargs.update(request.json)
        else:
            kwargs.update(request.form)

    if any(k.startswith('_') for k in kwargs.keys()):
        return abort(400, description="Underscore-prefixed arguments are not allowed")

    if pk:
        result = method(instance, **kwargs)

    else:
        result = method(**kwargs)

    return jsonify(result)


@api_bp.route('/<model_name>/<pk_number>/<method_name>')
def instance_level_method(model_name: str, pk_number: str, method_name: str):
    try:
        pk = int(pk_number)

    except ValueError:
        return abort(501)

    return method_execution(model_name, method_name, pk)


@api_bp.route('/<model_name>/<method_name>')
def class_level_method(model_name, method_name):
    return method_execution(model_name, method_name)
