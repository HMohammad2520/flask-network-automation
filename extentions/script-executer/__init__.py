from flask import Blueprint, render_template


bp = Blueprint('script-executer', __name__)


@bp.route('/')
def index():
    return render_template('script-executer/index.html')
