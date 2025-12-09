# ElfAgent API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required. API keys are configured server-side via environment variables.

## Endpoints

### Health Check

#### GET `/`

Basic health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "ElfAgent API",
  "version": "0.1.0"
}
```

#### GET `/health`

Detailed health status.

**Response:**
```json
{
  "status": "healthy",
  "runner_initialized": true,
  "session_service_initialized": true
}
```

### Query Processing

#### POST `/api/query`

Process a Christmas gift search query.

**Request Body:**
```json
{
  "query": "Christmas gift for a 10 year old boy who loves science",
  "user_id": "optional-user-id",
  "session_id": "optional-session-id"
}
```

**Parameters:**
- `query` (string, required): The gift search query
- `user_id` (string, optional): User identifier. Auto-generated if not provided
- `session_id` (string, optional): Session identifier. Auto-generated if not provided

**Response:**
```json
{
  "session_id": "uuid-string",
  "user_id": "uuid-string",
  "response": "Agent response with gift recommendations...",
  "status": "completed"
}
```

**Status Codes:**
- `200`: Success
- `500`: Internal server error
- `503`: Service not initialized

**Example:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Christmas gift for a 10 year old boy who loves science"
  }'
```

### Session Management

#### GET `/api/sessions/{user_id}`

Get all sessions for a specific user.

**Parameters:**
- `user_id` (string, required): User identifier

**Response:**
```json
{
  "user_id": "uuid-string",
  "sessions": [
    {
      "session_id": "uuid-string",
      "created_at": "timestamp",
      "messages": []
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/api/sessions/user-123
```

## WebSocket

### WS `/ws/query`

Real-time streaming query processing via WebSocket.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/query');
```

**Initial Message (Client → Server):**
```json
{
  "user_id": "optional-user-id",
  "session_id": "optional-session-id"
}
```

**Session Info Response (Server → Client):**
```json
{
  "type": "session_info",
  "user_id": "uuid-string",
  "session_id": "uuid-string"
}
```

**Query Message (Client → Server):**
```json
{
  "query": "Christmas gift for a 10 year old boy who loves science"
}
```

**Response Messages (Server → Client):**
```json
{
  "type": "response",
  "content": "Partial response text..."
}
```

**Completion Message (Server → Client):**
```json
{
  "type": "complete"
}
```

**Error Message (Server → Client):**
```json
{
  "error": "Error description"
}
```

**Example (JavaScript):**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/query');

ws.onopen = () => {
  // Send initial connection data
  ws.send(JSON.stringify({
    user_id: 'user-123',
    session_id: 'session-456'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'session_info') {
    console.log('Session:', data.session_id);
    
    // Send query
    ws.send(JSON.stringify({
      query: 'Christmas gift for a 10 year old boy who loves science'
    }));
  } else if (data.type === 'response') {
    console.log('Response:', data.content);
  } else if (data.type === 'complete') {
    console.log('Query complete');
  } else if (data.error) {
    console.error('Error:', data.error);
  }
};
```

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## CORS

CORS is enabled for the following origins:
- `http://localhost:3000` (Vite dev server)
- `http://localhost:5173` (Alternative Vite port)

## Rate Limiting

Currently no rate limiting implemented. Consider adding for production use.

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

```json
{
  "detail": "Error description"
}
```

Common error codes:
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error
- `503`: Service Unavailable

## Agent Workflow

When a query is processed:

1. **ProductSearchAgent**: Researches product features via Google Search
2. **VerificationAgent**: Requests user confirmation (if needed)
3. **MarketplaceAgent**: Coordinates marketplace searches
4. **MarketplaceSearchTeam**: Parallel searches on Amazon and Alibaba
5. **ProductAggregatorAgent**: Combines and ranks results
6. **ElfAgent**: Returns top 10 gift recommendations

## Response Format

Gift recommendations typically include:
- Product title
- Product description
- Original price
- Current price
- Star rating
- Product URL
- Product image
- Marketplace source (Amazon/Alibaba)

## Best Practices

1. **Reuse Sessions**: Use the same `session_id` for follow-up queries
2. **User Tracking**: Maintain consistent `user_id` for user history
3. **Error Handling**: Always handle potential errors and timeouts
4. **WebSocket**: Use WebSocket for better UX with streaming responses
5. **Timeouts**: Set appropriate timeouts (queries can take 30-60 seconds)

## Examples

### Python (requests)
```python
import requests

response = requests.post(
    'http://localhost:8000/api/query',
    json={'query': 'Christmas gift for a 10 year old boy who loves science'}
)
print(response.json())
```

### JavaScript (fetch)
```javascript
fetch('http://localhost:8000/api/query', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    query: 'Christmas gift for a 10 year old boy who loves science'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Christmas gift for a 10 year old boy who loves science"}'
```
