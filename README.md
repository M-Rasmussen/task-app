# React + Flask Skeleton

This is a minimal full-stack chat app with:

- A React frontend powered by Vite
- A Flask backend with CORS enabled
- A basic chat interface for sending and reading messages
- A root-level setup and dev workflow for Windows PowerShell

## Project structure

```text
frontend/   React app
backend/    Flask API
```

## Frontend setup

```powershell
cd frontend
npm install
npm run dev
```

The Vite dev server runs on `http://localhost:5173`.

## Backend setup

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The Flask API runs on `http://localhost:5000`.

## Quick start from the project root

```powershell
npm run setup
npm run dev
```

`npm run setup` installs frontend packages, creates `backend/.venv`, and installs Python dependencies.

`npm run dev` starts both the React dev server and the Flask backend together.

## Available API routes

- `GET /api/messages`
- `POST /api/messages`
- `GET /api/health`

## Notes

- The frontend defaults to calling `http://localhost:5000`.
- If you want a different backend URL, set `VITE_API_BASE_URL` in `frontend/.env`.
- The root scripts assume `npm`, `python`, and PowerShell are available on your PATH.
- Messages are stored in memory, so the chat history resets when the Flask server restarts.
