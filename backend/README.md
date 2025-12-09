# ElfAgent Backend API

AI-powered Christmas gift advisor backend with FastAPI.

## Setup

```bash
cd backend
uv sync --all-extras
```

## Environment Variables

Create `app/.env` file:

```
GOOGLE_API_KEY=your_google_api_key
RAPIDAPI_KEY=your_rapidapi_key
```

## Run

```bash
# Development server with auto-reload
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### REST API

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /api/query` - Process gift search query
- `GET /api/sessions/{user_id}` - Get user sessions

### WebSocket

- `WS /ws/query` - Streaming query responses

## Example Usage

```bash
# Health check
curl http://localhost:8000/health

# Query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Christmas gift for a 10 year old boy who loves science"}'
```

## Testing

```bash
uv run pytest
```
