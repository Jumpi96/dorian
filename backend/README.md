# Dorian Backend

A Flask-based backend server for the Dorian MVP project.

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

## Running the Server

To start the server:

```bash
python -m app.server
```

The server will run on http://localhost:3001

## Available Endpoints

- `GET /auth/login`: Returns a stubbed user ID
- `GET /auth/callback`: Returns a stubbed user ID

## Testing

To run the tests:

```bash
pytest
```

For test coverage:

```bash
pytest --cov=app
``` 