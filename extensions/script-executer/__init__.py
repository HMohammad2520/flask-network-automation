from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('script-executer', __name__)
bp.label = 'Automation'  # type: ignore
bp.description = 'Run Scripts and Automate workflows'  # type: ignore
bp.author = 'Devixa'  # type: ignore
bp.icon = 'S'  # type: ignore


@bp.route('/')
@login_required
def index():
    return render_template('script-executer/index.html')
