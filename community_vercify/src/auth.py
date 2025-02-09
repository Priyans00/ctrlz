from flask import Blueprint, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user as flask_login_user, logout_user, login_required, current_user
from supabase_client import supabase
from uuid import uuid4
from datetime import datetime

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    response = supabase.table('users').select('*').eq('id', user_id).execute()
    if response.data:
        user_data = response.data[0]
        return User(id=user_data['id'], username=user_data['username'], email=user_data['email'])
    return None

def register_user(username, email, password):
    # Check if the username or email already exists
    existing_user_response = supabase.table('users').select('*').or_(
        f"username.eq.{username},email.eq.{email}"
    ).execute()
    if existing_user_response.data:
        return {"error": "Username or email already exists"}

    user_id = str(uuid4())
    created_at = datetime.utcnow().isoformat()  # Convert datetime to string
    password = generate_password_hash(password, method='pbkdf2:sha256')
    response = supabase.table('users').insert({
        'id': user_id,
        'username': username,
        'email': email,
        'password': password,
        'created_at': created_at
    }).execute()
    if response.data is None:
        return {"error": response.error_message}
    return {"message": "User registered successfully"}

def authenticate_user(email, password):
    response = supabase.table('users').select('*').eq('email', email).execute()
    if not response.data:
        return {"error": "Invalid email or password"}

    user_data = response.data[0]
    if not check_password_hash(user_data['password'], password):
        return {"error": "Invalid email or password"}

    return {"message": "User authenticated successfully", "user_id": user_data['id']}

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout_user():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200