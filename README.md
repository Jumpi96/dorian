# Dorian MVP

A monorepo containing both frontend and backend components for the Dorian MVP project.

## Project Structure

```
dorian/
├── frontend/           # Node.js frontend application
├── backend/           # Python backend application
└── .github/          # GitHub configuration files
    └── workflows/    # GitHub Actions workflows
```

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run tests:
   ```bash
   npm test
   ```

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. Run tests:
   ```bash
   pytest
   ```

## CI/CD

The project uses GitHub Actions for continuous integration. The workflow runs on:
- Push to main branch
- Pull requests to main branch

The CI pipeline:
1. Runs frontend tests
2. Runs backend tests 