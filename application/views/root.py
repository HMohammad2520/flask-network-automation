from flask import Blueprint, redirect, url_for, jsonify
from application import get_version
from typing import Dict, Any

root_bp = Blueprint('root', 'root', url_prefix='/')

ATTRIBS: Dict[str, Any] = {
    'test': True,
    'version': get_version(),
}

@root_bp.route('/')
@root_bp.route('/website')
@root_bp.route('/website/<page>')
def index(page=None):
    return redirect(url_for(f'apps.website.{page or 'index'}'))

@root_bp.route('/favicon.ico')
def favicon():
    return redirect(url_for('apps.website.static', filename='favicon/favicon.ico'))

@root_bp.route('/.well-known/appspecific/com.chrome.devtools.json')
def chrome_dev_tools():
    return jsonify({})
