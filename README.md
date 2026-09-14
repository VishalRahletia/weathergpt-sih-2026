# WeatherGPT SIH 2026 MVP

A Pune-first, safety-oriented weather assistant. It retrieves structured data before composing a response; it never treats an LLM as a weather authority. English and Hindi are supported.

## Run locally
```powershell
cd weathergpt
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload
```
Open http://127.0.0.1:8000. Interactive API docs: http://127.0.0.1:8000/docs.

## Quality checks
```powershell
pytest backend/tests -q
python -m compileall backend/app
cd frontend; npm install; npm run lint; npm run typecheck; npm run build
```
For Docker: `docker compose up --build` (when Docker Desktop is installed).

The UI is a Vite frontend under `frontend/`; run `npm install` then `npm run dev`. Set `VITE_API_URL=http://127.0.0.1:8000` if needed.

## Hosted deployment
Deploy this repository root to Railway; it uses `Dockerfile` and `/health` for its health check. Deploy `frontend/` as a Vercel project, set `VITE_API_URL` to the Railway public API URL (without a trailing slash), then redeploy the frontend.

## Honest data policy
`WEATHER_PROVIDER=openmeteo` makes a live, unauthenticated request to Open-Meteo. If the request fails, or `WEATHER_PROVIDER=mock`, the UI labels deterministic demo data as **Mock / demo**. No official warnings are claimed: warnings are local rule-engine outputs unless an authorized official feed is added.

See [docs/architecture.md](docs/architecture.md), [docs/demo-script.md](docs/demo-script.md), [docs/requirements-checklist.md](docs/requirements-checklist.md), and [docs/limitations-roadmap.md](docs/limitations-roadmap.md).
