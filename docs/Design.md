# ElfAgent - System Design Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Diagrams](#component-diagrams)
4. [Data Flow Diagrams](#data-flow-diagrams)
5. [Agent Workflow](#agent-workflow)
6. [API Design](#api-design)
7. [Database Schema (Future)](#database-schema-future)

---

## System Overview

ElfAgent is an AI-powered Christmas gift advisor built with a microservices architecture, consisting of:
- **Backend**: FastAPI server with Google ADK hierarchical agent system
- **Frontend**: Next.js application with React 19 and Tailwind CSS
- **External APIs**: RapidAPI (Amazon, Alibaba), Google Search, Google Gemini LLM

### Technology Stack

**Backend:**
- Python 3.12+
- FastAPI (REST API)
- Google ADK (Agent Development Kit)
- LiteLLM (Multi-LLM support)
- aiohttp (Async HTTP client)
- uvicorn (ASGI server)

**Frontend:**
- Next.js 16 (App Router)
- React 19
- TypeScript 5.9
- Tailwind CSS 3.4
- Nx 22.2 (Monorepo)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Next.js Frontend (Port 4200)                 │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │  │
│  │  │   Page.tsx  │  │  Components  │  │  Config/Utils   │  │  │
│  │  │  (Layout)   │  │  - ChatMsg   │  │  - API Config   │  │  │
│  │  │             │  │  - Product   │  │  - Environment  │  │  │
│  │  │             │  │  - Snowflake │  │                 │  │  │
│  │  └─────────────┘  └──────────────┘  └─────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
                             │ (localhost:8000)
┌────────────────────────────▼────────────────────────────────────┐
│                      BACKEND API LAYER                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              FastAPI Server (Port 8000)                   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐  │  │
│  │  │  Endpoints   │  │  Middleware  │  │  Session Mgmt  │  │  │
│  │  │  - /api/query│  │  - CORS      │  │  - InMemory    │  │  │
│  │  │  - /health   │  │  - Logging   │  │  - Runner      │  │  │
│  │  │  - /ws/query │  │              │  │                │  │  │
│  │  └──────────────┘  └──────────────┘  └────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    AGENT ORCHESTRATION LAYER                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      ElfAgent (Root)                      │  │
│  │                    [LiteLLM Model]                        │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │            DirectorAgent (Sequential)               │ │  │
│  │  │                                                     │ │  │
│  │  │  ┌──────────────────┐  ┌──────────────────────┐   │ │  │
│  │  │  │ ProductSearch    │  │  MarketplaceAgent    │   │ │  │
│  │  │  │ Agent            │  │                      │   │ │  │
│  │  │  │ [Gemini Model]   │  │  [LiteLLM Model]     │   │ │  │
│  │  │  │                  │  │                      │   │ │  │
│  │  │  │ - Google Search  │  │  ┌────────────────┐ │   │ │  │
│  │  │  │ - Feature        │  │  │ Marketplace    │ │   │ │  │
│  │  │  │   Analysis       │  │  │ Coordinator    │ │   │ │  │
│  │  │  │                  │  │  │ (Sequential)   │ │   │ │  │
│  │  │  └──────────────────┘  │  │                │ │   │ │  │
│  │  │                        │  │ ┌────────────┐ │ │   │ │  │
│  │  │                        │  │ │ Marketplace│ │ │   │ │  │
│  │  │                        │  │ │ SearchTeam │ │ │   │ │  │
│  │  │                        │  │ │ (Parallel) │ │ │   │ │  │
│  │  │                        │  │ │            │ │ │   │ │  │
│  │  │                        │  │ │ ┌────────┐ │ │ │   │ │  │
│  │  │                        │  │ │ │ Amazon │ │ │ │   │ │  │
│  │  │                        │  │ │ │ Agent  │ │ │ │   │ │  │
│  │  │                        │  │ │ └────────┘ │ │ │   │ │  │
│  │  │                        │  │ │ ┌────────┐ │ │ │   │ │  │
│  │  │                        │  │ │ │Alibaba │ │ │ │   │ │  │
│  │  │                        │  │ │ │ Agent  │ │ │ │   │ │  │
│  │  │                        │  │ │ └────────┘ │ │ │   │ │  │
│  │  │                        │  │ └────────────┘ │ │   │ │  │
│  │  │                        │  │                │ │   │ │  │
│  │  │                        │  │ ┌────────────┐ │ │   │ │  │
│  │  │                        │  │ │ Product    │ │ │   │ │  │
│  │  │                        │  │ │ Aggregator │ │ │   │ │  │
│  │  │                        │  │ │ Agent      │ │ │   │ │  │
│  │  │                        │  │ └────────────┘ │ │   │ │  │
│  │  │                        │  └────────────────┘ │   │ │  │
│  │  │                        └──────────────────────┘   │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    EXTERNAL SERVICES LAYER                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   RapidAPI   │  │ Google APIs  │  │   LLM Providers      │  │
│  │              │  │              │  │                      │  │
│  │ - Amazon API │  │ - Search API │  │ - Google Gemini      │  │
│  │ - Alibaba API│  │              │  │ - OpenAI (via        │  │
│  │              │  │              │  │   LiteLLM)           │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Diagrams

### Backend Components

```
┌─────────────────────────────────────────────────────────────┐
│                      Backend Structure                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │                    app/main.py                     │    │
│  │  - FastAPI application                             │    │
│  │  - Lifespan management                             │    │
│  │  - CORS configuration                              │    │
│  │  - Endpoint definitions                            │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                  │
│         ┌────────────────┼────────────────┐                │
│         │                │                │                │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐         │
│  │ elfagent/   │  │   tools/    │  │   utils/   │         │
│  │             │  │             │  │            │         │
│  │ agent.py    │  │ awstools.py │  │ utility.py │         │
│  │ - Builders  │  │ alibaba...  │  │ const.py   │         │
│  │ - Agents    │  │ agent...    │  │ - Config   │         │
│  │             │  │             │  │ - Session  │         │
│  └─────────────┘  └─────────────┘  └────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Frontend Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Structure                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │              apps/chat/src/app/                    │    │
│  │                                                    │    │
│  │  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  page.tsx    │  │  layout.tsx  │              │    │
│  │  │  (Main Page) │  │  (Root)      │              │    │
│  │  └──────────────┘  └──────────────┘              │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                  │
│         ┌────────────────┼────────────────┐                │
│         │                │                │                │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐         │
│  │ components/ │  │    lib/     │  │   public/  │         │
│  │             │  │             │  │            │         │
│  │ chat_       │  │ config.ts   │  │ elf_icon   │         │
│  │ interface   │  │ - API URLs  │  │ elf_avatar │         │
│  │             │  │ - Env vars  │  │ favicon    │         │
│  │ chat_       │  │             │  │            │         │
│  │ message     │  └─────────────┘  └────────────┘         │
│  │             │                                           │
│  │ product_    │                                           │
│  │ card        │                                           │
│  │             │                                           │
│  │ snowflakes  │                                           │
│  └─────────────┘                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Query Processing Flow

```
┌──────┐                                                    ┌──────────┐
│ User │                                                    │ External │
│      │                                                    │   APIs   │
└───┬──┘                                                    └────┬─────┘
    │                                                            │
    │ 1. Enter gift query                                       │
    │                                                            │
    ▼                                                            │
┌────────────┐                                                  │
│  Frontend  │                                                  │
│  (React)   │                                                  │
└─────┬──────┘                                                  │
      │                                                          │
      │ 2. POST /api/query                                      │
      │    { query, user_id, session_id }                       │
      │                                                          │
      ▼                                                          │
┌────────────┐                                                  │
│  FastAPI   │                                                  │
│  Endpoint  │                                                  │
└─────┬──────┘                                                  │
      │                                                          │
      │ 3. Initialize/Get Session                               │
      │                                                          │
      ▼                                                          │
┌────────────┐                                                  │
│  Runner    │                                                  │
│  (ADK)     │                                                  │
└─────┬──────┘                                                  │
      │                                                          │
      │ 4. Execute ElfAgent                                     │
      │                                                          │
      ▼                                                          │
┌────────────────────────────────────────────────────────────┐ │
│                    Agent Workflow                          │ │
│                                                            │ │
│  ┌──────────────────────────────────────────────────────┐ │ │
│  │ Step 1: ProductSearchAgent                           │ │ │
│  │  - Analyze query                                     │ │ │
│  │  - Google Search for product features ──────────────┼─┼─┤
│  │  - Extract top 5 features                           │ │ │
│  │  - Determine product names                          │ │ │
│  └──────────────────────────────────────────────────────┘ │ │
│                          │                                 │ │
│                          ▼                                 │ │
│  ┌──────────────────────────────────────────────────────┐ │ │
│  │ Step 2: MarketplaceAgent                             │ │ │
│  │                                                      │ │ │
│  │  ┌────────────────────────────────────────────────┐ │ │ │
│  │  │ MarketplaceSearchTeam (Parallel)               │ │ │ │
│  │  │                                                │ │ │ │
│  │  │  ┌──────────────┐      ┌──────────────┐      │ │ │ │
│  │  │  │ AmazonAgent  │      │ AlibabaAgent │      │ │ │ │
│  │  │  │ - Search IT  │      │ - Search IT  │      │ │ │ │
│  │  │  │ - Get deals ─┼──────┼──────────────┼──────┼─┼─┤
│  │  │  │ - Top 10     │      │ - Top 10     │      │ │ │ │
│  │  │  └──────────────┘      └──────────────┘      │ │ │ │
│  │  └────────────────────────────────────────────────┘ │ │ │
│  │                          │                           │ │ │
│  │                          ▼                           │ │ │
│  │  ┌────────────────────────────────────────────────┐ │ │ │
│  │  │ ProductAggregatorAgent                         │ │ │ │
│  │  │ - Combine results                              │ │ │ │
│  │  │ - Remove duplicates                            │ │ │ │
│  │  │ - Sort by discount & gift suitability         │ │ │ │
│  │  │ - Return top 20 deals                          │ │ │ │
│  │  └────────────────────────────────────────────────┘ │ │ │
│  └──────────────────────────────────────────────────────┘ │ │
│                          │                                 │ │
│                          ▼                                 │ │
│  ┌──────────────────────────────────────────────────────┐ │ │
│  │ Step 3: ElfAgent (Final Processing)                  │ │ │
│  │  - Select top 10 deals                               │ │ │
│  │  - Sort by quality/price ratio                       │ │ │
│  │  - Format as JSON                                    │ │ │
│  └──────────────────────────────────────────────────────┘ │ │
└────────────────────────────────────────────────────────────┘ │
      │                                                          │
      │ 5. Return response                                      │
      │                                                          │
      ▼                                                          │
┌────────────┐                                                  │
│  Frontend  │                                                  │
│  Display   │                                                  │
└────────────┘                                                  │
```

### Session Management Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Session Lifecycle                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. First Request                                           │
│     ┌──────────────────────────────────────────┐           │
│     │ No session_id provided                   │           │
│     │ → Generate new UUID                      │           │
│     │ → Create InMemorySession                 │           │
│     │ → Return session_id to client            │           │
│     └──────────────────────────────────────────┘           │
│                                                             │
│  2. Subsequent Requests                                     │
│     ┌──────────────────────────────────────────┐           │
│     │ session_id provided                      │           │
│     │ → Retrieve existing session              │           │
│     │ → Append new message                     │           │
│     │ → Maintain conversation context          │           │
│     └──────────────────────────────────────────┘           │
│                                                             │
│  3. Session Storage (Current: In-Memory)                    │
│     ┌──────────────────────────────────────────┐           │
│     │ InMemorySessionService                   │           │
│     │ - Volatile storage                       │           │
│     │ - Lost on server restart                 │           │
│     │ - No persistence                         │           │
│     └──────────────────────────────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent Workflow

### Hierarchical Agent Structure

```
ElfAgent (Root)
│
└─── DirectorAgent (Sequential)
     │
     ├─── ProductSearchAgent
     │    │
     │    └─── Tools:
     │         └─── google_search
     │
     └─── MarketplaceAgent
          │
          └─── MarketplaceCoordinator (Sequential)
               │
               ├─── MarketplaceSearchTeam (Parallel)
               │    │
               │    ├─── AmazonAgent
               │    │    └─── Tools:
               │    │         └─── get_amazon_deals_by_product
               │    │
               │    └─── AlibabaAgent
               │         └─── Tools:
               │              └─── get_alibaba_deals_by_product
               │
               └─── ProductAggregatorAgent
```

### Agent Responsibilities

| Agent | Type | Model | Responsibility |
|-------|------|-------|----------------|
| **ElfAgent** | Root | LiteLLM | Final selection of top 10 gifts, JSON formatting |
| **DirectorAgent** | Sequential | N/A | Orchestrates workflow between agents |
| **ProductSearchAgent** | Worker | Gemini | Google Search for product features and analysis |
| **MarketplaceAgent** | Coordinator | LiteLLM | Manages marketplace search workflow |
| **MarketplaceCoordinator** | Sequential | N/A | Coordinates search and aggregation |
| **MarketplaceSearchTeam** | Parallel | N/A | Executes parallel marketplace searches |
| **AmazonAgent** | Worker | Gemini | Amazon marketplace search (IT locale) |
| **AlibabaAgent** | Worker | Gemini | Alibaba marketplace search (IT locale) |
| **ProductAggregatorAgent** | Worker | LiteLLM | Combines, deduplicates, and ranks results |

---

## API Design

### REST Endpoints

#### POST /api/query
Process a gift search query.

**Request:**
```json
{
  "query": "Christmas gift for a 10 year old boy who loves science",
  "user_id": "optional-uuid",
  "session_id": "optional-uuid"
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "user_id": "uuid",
  "response": "JSON string with gift recommendations",
  "status": "completed"
}
```

#### GET /health
Health check with service status.

**Response:**
```json
{
  "status": "healthy",
  "runner_initialized": true,
  "session_service_initialized": true
}
```

### WebSocket Endpoint

#### WS /ws/query
Real-time streaming responses (currently not fully implemented in frontend).

**Message Flow:**
1. Client connects
2. Client sends: `{ "user_id": "...", "session_id": "..." }`
3. Server responds: `{ "type": "session_info", "user_id": "...", "session_id": "..." }`
4. Client sends: `{ "query": "..." }`
5. Server streams: `{ "type": "response", "content": "..." }`
6. Server completes: `{ "type": "complete" }`

## Security Considerations

### Current Implementation
- API keys stored in environment variables
- CORS restricted to localhost origins
- No authentication/authorization
- In-memory sessions (no persistence)

### Recommended Improvements
- Add JWT-based authentication
- Implement rate limiting
- Add request validation and sanitization
- Use secrets management service (AWS Secrets Manager, HashiCorp Vault)
- Add HTTPS/TLS in production
- Implement API key rotation
- Add logging and monitoring

---

## Scalability Considerations

### Current Limitations
- Single server instance
- In-memory session storage
- No load balancing
- No caching layer
- Synchronous external API calls

### Recommended Improvements
- Horizontal scaling with load balancer
- Redis for session storage
- CDN for static assets
- API response caching
- Message queue for async processing
- Database connection pooling
- Microservices architecture for agents

---

## Monitoring and Observability

### Recommended Metrics
- Request latency (p50, p95, p99)
- Error rates by endpoint
- Agent execution time
- External API response times
- Session duration
- User query patterns
- Cache hit rates

### Recommended Tools
- Prometheus + Grafana for metrics
- ELK Stack for logging
- Sentry for error tracking
- OpenTelemetry for distributed tracing
