from flask import Blueprint, abort

apps_bp = Blueprint('apps', __name__)


@apps_bp.route('/')
def index():
    return abort(404)
