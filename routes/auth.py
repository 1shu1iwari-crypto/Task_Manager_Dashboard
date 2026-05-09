from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
        
    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'error')
        return redirect(url_for('pages.register'))
        
    new_user = User(username=username)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    flash('Registration successful. Please login.', 'success')
    return redirect(url_for('pages.login'))

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('pages.dashboard'))
        
    flash('Invalid username or password', 'error')
    return redirect(url_for('pages.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('pages.login'))
