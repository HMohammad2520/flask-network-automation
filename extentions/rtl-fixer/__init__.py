from flask import Blueprint, render_template

bp = Blueprint('rtl-fixer', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


__all__ = ['bp']
