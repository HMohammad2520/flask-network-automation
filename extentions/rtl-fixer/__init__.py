from flask import Blueprint, render_template

bp = Blueprint('rtl-fixer', __name__)


@bp.route('/')
def index():
    return render_template('rtl-fixer/index.html')


__all__ = ['bp']
