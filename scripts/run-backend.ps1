$ErrorActionPreference = "Stop"

if (-not (Test-Path "backend/.venv/Scripts/python.exe")) {
    throw "Backend virtual environment not found. Run 'npm run setup' first."
}

& "backend/.venv/Scripts/python.exe" "backend/app.py"

