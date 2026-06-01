from flask import Blueprint, redirect, render_template, url_for

website = Blueprint('website', 'website', url_prefix='/website', template_folder='application/templates')

@website.route('/')
def index():
    return redirect(url_for('website.home'))

@website.route('/home')
def home():
    breadcrumbs = [
        {'name': 'Home', 'url': None},
    ]
    return render_template('home.html', breadcrumbs=breadcrumbs)

@website.route('/contact')
def contact():
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('website.home')},
        {'name': 'Contact', 'url': None},
    ]
    return render_template('contact.html', breadcrumbs=breadcrumbs)

@website.route('/about')
def about():
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('website.home')},
        {'name': 'About', 'url': None},
    ]
    return render_template('about.html', breadcrumbs=breadcrumbs)

@website.route('/faq')
def faq():
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('website.home')},
        {'name': 'FAQ', 'url': None},
    ]
    return render_template('faq.html', breadcrumbs=breadcrumbs)