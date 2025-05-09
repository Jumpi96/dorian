import jwt
from flask import request, url_for, redirect, jsonify
from functools import wraps
from datetime import datetime, timedelta, UTC
from app.config import Config

JWT_SECRET = Config.JWT_SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

def init_auth_routes(app, google):
    @app.route('/auth/login')
    def login():
        redirect_uri = url_for('auth_callback', _external=True)
        return google.authorize_redirect(redirect_uri)

    @app.route('/auth/callback')
    def auth_callback():
        google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()

        payload = {
            'sub': user_info['id'],
            'email': user_info['email'],
            'name': user_info.get('name'),
            'exp': datetime.now(UTC) + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }

        jwt_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        frontend_redirect = f"{Config.FRONTEND_REDIRECT_SUCCESS}?token={jwt_token}"
        return redirect(frontend_redirect)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header:
            return jsonify({"error": "Missing Authorization Header"}), 401
        
        parts = auth_header.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            return jsonify({"error": "Invalid Authorization Header"}), 401

        token = parts[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        request.user = payload
        return f(*args, **kwargs)
    return decorated
