from flask import Blueprint, render_template, abort

apps_bp = Blueprint('apps', 'apps', url_prefix='/apps')

@apps_bp.route('/')
def index():
    return abort(404)
