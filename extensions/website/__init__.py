from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint('website', __name__)
bp.label = 'Web Application'  #type: ignore
bp.description = 'Devixa website'  #type: ignore
bp.author = 'Devixa'  #type: ignore
bp.icon = 'W' #type: ignore


@bp.route('/')
def index():
    return redirect(url_for('apps.website.home'))


@bp.route('/home')
def home():
    breadcrumbs = [
        {'name': 'Home', 'url': None},
    ]
    return render_template('website/home.html', breadcrumbs=breadcrumbs)


@bp.route('/contact')
def contact():
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('apps.website.home')},
        {'name': 'Contact', 'url': None},
    ]
    return render_template('website/contact.html', breadcrumbs=breadcrumbs)


@bp.route('/about')
def about():
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('apps.website.home')},
        {'name': 'About', 'url': None},
    ]
    return render_template('website/about.html', breadcrumbs=breadcrumbs)


@bp.route('/faq')
def faq():
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('apps.website.home')},
        {'name': 'FAQ', 'url': None},
    ]
    return render_template('website/faq.html', breadcrumbs=breadcrumbs)


__all__ = ['bp']
