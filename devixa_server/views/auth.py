from flask import Blueprint, request, abort, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user
from ..models import User
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return abort(403)
        
        user: User|None = User.query.filter(User.username==username).first()
        if user is None:
            return abort(404)

        if password == user.password:
            login_user(user)

        return redirect(url_for('apps.index'))

    elif request.method == 'GET':
        return render_template('auth/login.html')

    else:
        return abort(402)

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user is not None and current_user.is_authenticated:
        logout_user()
        return redirect(url_for('apps.index'))

    token = request.form.get('token', '')
    if not token:
        return abort(403)

    return token