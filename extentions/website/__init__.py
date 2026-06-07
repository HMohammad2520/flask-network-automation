from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint('website', __name__)


@bp.route('/')
def index():
    return redirect(url_for('apps.website.home'))


@bp.route('/home')
def home():
    breadcrumbs = [
        {'name': 'Home', 'url': None},
    ]
    return render_template('home.html', breadcrumbs=breadcrumbs)


@bp.route('/contact')
def contact():
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('apps.website.home')},
        {'name': 'Contact', 'url': None},
    ]
    return render_template('contact.html', breadcrumbs=breadcrumbs)


@bp.route('/about')
def about():
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('apps.website.home')},
        {'name': 'About', 'url': None},
    ]
    return render_template('about.html', breadcrumbs=breadcrumbs)


@bp.route('/faq')
def faq():
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('apps.website.home')},
        {'name': 'FAQ', 'url': None},
    ]
    return render_template('faq.html', breadcrumbs=breadcrumbs)


__all__ = ['bp']
