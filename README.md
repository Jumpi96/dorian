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

The frontend is a modern web application built with Next.js 15, React 19, and TypeScript. It uses Radix UI components and is styled with Tailwind CSS.

### Prerequisites
- Node.js (Latest LTS version recommended)
- pnpm (Package manager)

### Getting Started

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Run the development server:
   ```bash
   pnpm dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

### Available Scripts
- `pnpm dev` - Start the development server
- `pnpm build` - Build the application for production
- `pnpm start` - Start the production server
- `pnpm lint` - Run ESLint to check code quality

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