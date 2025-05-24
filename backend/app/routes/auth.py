import jwt
from flask import request, url_for, redirect, jsonify
from functools import wraps
from datetime import datetime, timedelta, timezone
from app.config import Config

JWT_SECRET = Config.JWT_SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

def init_auth_routes(app, google):
    @app.route('/auth/login')
    def login():
        redirect_uri = url_for('auth_callback', _external=True)
        print(f"[Auth Login] Redirect URI: {redirect_uri}")
        return google.authorize_redirect(redirect_uri)

    @app.route('/auth/callback')
    def auth_callback():
        print("[Auth Callback] Starting callback process")
        try:
            google.authorize_access_token()
            resp = google.get('userinfo')
            user_info = resp.json()
            print(f"[Auth Callback] User info received: {user_info.get('email')}")

            payload = {
                'sub': user_info['id'],
                'email': user_info['email'],
                'name': user_info.get('name'),
                'exp': datetime.now(timezone.utc) + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }

            jwt_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            print(f"[Auth Callback] JWT token generated: {jwt_token[:10]}...")
            
            location = Config.FRONTEND_REDIRECT_SUCCESS
            print(f"[Auth Callback] Redirect URL: {location}")
            
            # Build cookie string manually
            cookie_str = (
                f"auth_token={jwt_token}; "
                f"Domain={Config.COOKIE_DOMAIN}; "
                "Path=/; "
                "Secure; "
                "HttpOnly; "
                "SameSite=None; "
                f"Max-Age={JWT_EXP_DELTA_SECONDS}"
            )
            print(f"[Auth Callback] Cookie string: {cookie_str}")

            # Return explicit API Gateway v1.0 format
            return {
                "statusCode": 302,
                "headers": {"Location": location},
                "multiValueHeaders": {
                    "Set-Cookie": [cookie_str]
                }
            }
        except Exception as e:
            print(f"[Auth Callback] Error: {str(e)}")
            raise

    @app.route('/auth/verify')
    @requires_auth
    def verify_token():
        return jsonify({"status": "valid"}), 200

    return app

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
