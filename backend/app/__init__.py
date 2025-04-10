from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)
    
    @app.route('/auth/login', methods=['GET'])
    def login():
        return jsonify({"user": "fakeUserId"})
    
    @app.route('/auth/callback', methods=['GET'])
    def callback():
        return jsonify({"user": "fakeUserId"})
    
    return app 