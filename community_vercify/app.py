from flask import Flask, flash, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from waitress import serve
from src.auth import auth_bp, login_manager, User
from custom_json_encoder import CustomJSONEncoder

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for CSRF protection
CORS(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize the login manager
login_manager.init_app(app)

# Register the authentication blueprint
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Set the custom JSON encoder
app.json_encoder = CustomJSONEncoder

from routes import routes_bp
app.register_blueprint(routes_bp)

@app.route('/')
def home():
    return jsonify(message="Hello, World!")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('routes.home'))


    app.run(host="0.0.0.0", port=5000)