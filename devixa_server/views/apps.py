from flask import Blueprint, render_template

apps_bp = Blueprint('apps', __name__)


@apps_bp.route('/')
def index():
    apps = [bp for bp, _ in apps_bp._blueprints]
    return render_template('apps/index.html', apps=apps)
