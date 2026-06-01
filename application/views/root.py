from flask import Blueprint, request, redirect, url_for, jsonify, abort
from application import get_version
from typing import Dict, Any

root = Blueprint('root', 'root', url_prefix='/')

ATTRIBS: Dict[str, Any] = {
    'test': True,
    'version': get_version(),
}


@root.route('/')
def index():
    return redirect(url_for('website.index'))


@root.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon/favicon.ico'))


@root.route('/.well-known/appspecific/com.chrome.devtools.json')
def chrome_dev_tools():
    return jsonify({})
