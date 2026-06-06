from flask import Blueprint, request, abort

auth_bp = Blueprint('auth', 'auth', url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or password:
        return abort(403)

    return 'TEST_TOKEN'

@auth_bp.route('/logout', methods=['POST'])
def logout():
    token = request.form.get('token', '')
    if not token:
        return abort(403)

    return token