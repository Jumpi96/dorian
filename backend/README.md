# Dorian Backend

A Flask-based backend server for the Dorian MVP project with Google OAuth authentication.

## Setup

1. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On Unix or MacOS
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the required values:
     - `GOOGLE_CLIENT_ID`: Your Google OAuth client ID
     - `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret
     - `GOOGLE_REDIRECT_URI`: http://localhost:3001/auth/callback
     - `JWT_SECRET_KEY`: A secure random string for JWT signing
     - AWS credentials for DynamoDB access

## Google OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to Credentials
5. Create an OAuth 2.0 Client ID
6. Add authorized redirect URIs:
   - http://localhost:3001/auth/callback
7. Copy the client ID and client secret to your `.env` file

## Running the Server

To start the server:

```bash
python -m app.server
```

The server will run on http://localhost:3001

## Available Endpoints

- `GET /auth/login`: Returns OAuth configuration for client-side redirect
- `GET /auth/callback`: Handles OAuth callback and returns JWT token

## Testing

To run the tests:

```bash
pytest
```

For test coverage:

```bash
pytest --cov=app
```

## Authentication Flow

1. Client calls `/auth/login` to get OAuth configuration
2. Client redirects user to Google's consent screen
3. Google redirects back to `/auth/callback` with authorization code
4. Server exchanges code for token and verifies with Google
5. Server creates/updates user in DynamoDB
6. Server returns JWT token to client 