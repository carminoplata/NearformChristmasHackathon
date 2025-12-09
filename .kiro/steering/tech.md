# Technology Stack

## Build System

- **Package Manager**: uv (backend), npm (frontend)
- **Python Version**: >=3.12
- **Build Backend**: hatchling

## Backend Dependencies

### Core
- **google-adk** (1.18.0): Google Agent Development Kit for building AI agents
- **litellm** (1.79.1): LLM integration library
- **fastapi** (>=0.115.0): Modern web framework for building APIs
- **uvicorn[standard]** (>=0.32.0): ASGI server
- **aiohttp** (>=3.13.2, <4.0.0): Async HTTP client for API calls
- **python-dotenv** (>=1.0.0): Environment variable management
- **websockets** (>=14.0): WebSocket support

### Development
- **pytest** (>=9.0.1): Testing framework
- **pytest-asyncio** (>=1.3.0): Async test support
- **httpx** (>=0.27.0): HTTP client for testing

## Frontend Dependencies

### Core
- **next** (~16.0.1): React framework with SSR and App Router
- **react** (^19.0.0): UI library
- **react-dom** (^19.0.0): React DOM rendering
- **tailwindcss** (3.4.3): Utility-first CSS framework

### Development & Build Tools
- **nx** (22.2.0): Monorepo build system with intelligent caching
- **@nx/next** (22.2.0): Nx Next.js plugin
- **@nx/playwright** (22.2.0): E2E testing with Playwright
- **@nx/jest** (22.2.0): Jest testing integration
- **typescript** (~5.9.2): TypeScript compiler
- **typescript-eslint** (^8.40.0): TypeScript ESLint support
- **jest** (^30.0.2): Testing framework
- **@testing-library/react** (16.3.0): React testing utilities
- **@playwright/test** (^1.36.0): Playwright test runner
- **eslint** (^9.8.0): Code linting
- **eslint-config-next** (^16.0.1): Next.js ESLint configuration
- **eslint-config-prettier** (^10.0.0): Prettier ESLint integration
- **prettier** (^2.6.2): Code formatting
- **postcss** (8.4.38): CSS processing
- **autoprefixer** (10.4.13): CSS vendor prefixing
- **@swc/core** (~1.5.7): Fast TypeScript/JavaScript compiler

## External APIs

- **RapidAPI**: Used for marketplace data
  - Amazon Real-Time Data API
  - AliExpress DataHub API
- **Google Gemini**: LLM model (gemini-1.5-pro)
- **Google Search**: Product research via ADK tools

## Environment Variables Required

- `GOOGLE_API_KEY`: Google Gemini API access
- `RAPIDAPI_KEY`: RapidAPI marketplace access

## Common Commands

### Backend
```bash
cd backend

# Install dependencies
uv sync --all-extras

# Run API server (development)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run API server (production)
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run tests
uv run pytest

# Run specific test
uv run pytest tests/units/tools/test_awstools.py
```

### Frontend (Nx with Next.js)
```bash
cd frontend

# Install dependencies
npm install

# Run development server
nx dev chat
# Runs on http://localhost:4200 (default Nx port)

# Build for production
nx build chat

# Start production server
nx start chat

# Lint
nx lint chat

# Run tests
nx test chat

# Run E2E tests
nx e2e chat-e2e

# Show dependency graph
nx graph

# Clear Nx cache
nx reset
```

## Key Technical Patterns

### Backend
- Async/await throughout for concurrent operations
- Agent-based architecture with sequential and parallel workflows
- Tool-based function calling for agent capabilities
- Session-based conversation management with resumability
- RESTful API design with FastAPI
- WebSocket support for streaming responses
- CORS-enabled for frontend communication

### Frontend
- Next.js App Router with server-side rendering (SSR)
- React 19 component-based UI architecture with TypeScript
- Nx monorepo with intelligent build caching and task orchestration
- Tailwind CSS configured for utility-first styling
- Playwright for E2E testing
- Jest for unit testing
- ESLint and Prettier for code quality
- Currently minimal implementation - full UI features to be developed
