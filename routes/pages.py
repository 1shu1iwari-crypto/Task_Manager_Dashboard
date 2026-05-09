from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from services.analytics import get_task_analytics

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('pages.dashboard'))
    return redirect(url_for('pages.login'))

@pages_bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pages.dashboard'))
    return render_template('login.html')

@pages_bp.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('pages.dashboard'))
    return render_template('register.html')

@pages_bp.route('/dashboard')
@login_required
def dashboard():
    analytics = get_task_analytics(current_user.id)
    return render_template('dashboard.html', user=current_user, analytics=analytics)
