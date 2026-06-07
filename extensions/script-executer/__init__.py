from flask import Blueprint, render_template


bp = Blueprint('script-executer', __name__)
bp.label = 'Automation'  # type: ignore
bp.description = 'Run Scripts and Automate workflows'  # type: ignore
bp.author = 'Devixa'  # type: ignore
bp.icon = 'S'  # type: ignore


@bp.route('/')
def index():
    return render_template('script-executer/index.html')
