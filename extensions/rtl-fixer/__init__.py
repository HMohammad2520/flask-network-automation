from flask import Blueprint, render_template

bp = Blueprint('rtl-fixer', __name__)
bp.label = 'Text Editing'  # type: ignore
bp.description = 'Fix rtl problems'  # type: ignore
bp.author = 'Devixa'  # type: ignore
bp.icon = 'R'  # type: ignore


@bp.route('/')
def index():
    return render_template('rtl-fixer/index.html')


__all__ = ['bp']
