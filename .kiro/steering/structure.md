# Project Structure

## Directory Organization

```
.
├── frontend/                       # Nx monorepo with Next.js
│   ├── apps/
│   │   ├── chat/                   # Main Next.js application
│   │   │   ├── src/
│   │   │   │   └── app/
│   │   │   │       ├── api/        # API routes
│   │   │   │       ├── page.tsx    # Main page
│   │   │   │       ├── layout.tsx  # Root layout
│   │   │   │       └── global.css  # Global styles
│   │   │   ├── public/             # Static assets
│   │   │   ├── next.config.js
│   │   │   ├── tailwind.config.js
│   │   │   └── package.json
│   │   └── chat-e2e/               # E2E tests with Playwright
│   │       ├── src/
│   │       └── playwright.config.ts
│   ├── nx.json
│   ├── package.json
│   └── tsconfig.base.json
│
└── backend/                        # Python FastAPI backend
    ├── .venv/                      # Virtual environment
    ├── app/
    │   ├── .env                    # Environment variables
    │   ├── .env.example
    │   ├── __init__.py
    │   ├── main.py                 # FastAPI application entry
    │   ├── elfagent/
    │   │   ├── __init__.py
    │   │   └── agent.py            # Agent definitions and builders
    │   ├── tools/                  # External API integrations
    │   │   ├── __init__.py
    │   │   ├── agenttools.py       # Agent-specific tools
    │   │   ├── alibabatools.py     # Alibaba API integration
    │   │   └── awstools.py         # Amazon API integration
    │   └── utils/
    │       ├── __init__.py
    │       ├── const.py            # Constants and env vars
    │       └── utility.py          # Session management, LLM config
    ├── tests/
    │   ├── __init__.py
    │   ├── e2e/
    │   │   └── __init__.py
    │   ├── integrations/
    │   │   ├── __init__.py
    │   │   └── test_api.py         # API integration tests
    │   └── units/
    │       ├── __init__.py
    │       └── tools/              # Tool-specific tests
    │           ├── __init__.py
    │           └── test_awstools.py
    ├── pyproject.toml              # Project config and dependencies
    └── uv.lock                     # Dependency lock file
```

## Module Breakdown

### `backend/app/elfagent`
Contains agent factory functions that build the hierarchical agent system:
- `build_amazon_agent()`: Amazon marketplace search agent
- `build_alibaba_agent()`: Alibaba marketplace search agent
- `build_root_agent()`: Top-level coordinator
- `build_markeplace_agent()`: Marketplace coordination layer
- `build_verification_agent()`: User confirmation handler
- `google_agent()`: Product research agent

Module exports pre-configured `root_agent` for use in main application.

### `backend/app/tools/`
API integration modules with async functions:
- `agenttools.py`: Agent-specific tools (user confirmation)
- `awstools.py`: Amazon API integration via RapidAPI
- `alibabatools.py`: Alibaba API integration via RapidAPI

All tool functions are async and use aiohttp for HTTP requests.

### `backend/app/utils/`
Shared utilities:
- `utility.py`: Session management, LLM configuration, retry logic
- `const.py`: Environment variable loading and constants

### `backend/app/main.py`
FastAPI application entry point that:
1. Initializes environment and validates API keys on startup
2. Creates App with root_agent and resumability config
3. Sets up InMemorySessionService and Runner
4. Exposes REST API endpoints:
   - `GET /` - Health check
   - `GET /health` - Detailed health status
   - `POST /api/query` - Process gift search queries
   - `GET /api/sessions/{user_id}` - Get user sessions
5. Provides WebSocket endpoint:
   - `WS /ws/query` - Streaming query responses
6. Includes CORS middleware for frontend communication

## Import Conventions

- Relative imports within packages (e.g., `from agents import root_agent`)
- Absolute imports from top-level modules (e.g., `from tools import get_amazon_deals_by_product`)
- Google ADK imports grouped together
- Third-party imports before local imports

## Naming Conventions

- **Agents**: Suffix with `_agent` or `Agent` (e.g., `amazon_agent`, `BestDealsAgent`)
- **Functions**: Snake_case for all functions
- **Tool functions**: Prefix with action verb (e.g., `get_amazon_deals_by_product`, `ask_confirmation`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `RAPIDAPI_API_KEY`, `AMAZON_API_URL`)

### `frontend/` (Nx Monorepo with Next.js)
Next.js-based web interface built with Nx:
- `apps/chat/`: Main application directory
  - `src/app/page.tsx`: Main page component with Christmas-themed UI
  - `src/app/layout.tsx`: Root layout component
  - `src/app/global.css`: Global styles with Tailwind CSS
  - `src/app/api/`: API routes directory
  - `src/components/`: React components
    - `chat_interface.tsx`: Main chat interface with API integration
    - `chat_message.tsx`: Chat message display component
    - `gift_card.tsx`: Product/gift card component
    - `snowflakes.tsx`: Animated snowflakes effect
  - `src/lib/`: Utility functions and configuration
    - `config.ts`: API endpoint configuration
  - `src/types/`: TypeScript type definitions
    - `index.ts`: Shared interfaces (Gift, Message, ApiResponse, etc.)
  - `public/`: Static assets (images, icons)
  - `next.config.js`: Next.js configuration
  - `tailwind.config.js`: Tailwind CSS configuration
  - `postcss.config.js`: PostCSS configuration
  - `package.json`: App-specific dependencies
- `apps/chat-e2e/`: E2E test suite with Playwright
  - `src/example.spec.ts`: Example E2E test
  - `playwright.config.ts`: Playwright configuration
- `nx.json`: Nx workspace configuration
- `tsconfig.base.json`: Base TypeScript configuration
- `package.json`: Root workspace dependencies

Frontend structure notes:
- App name is `@frontend/chat` (not christmas-chat)
- Centralized type definitions in `src/types/index.ts`
- TypeScript support configured
- Nx build caching and optimization enabled
- Server-side rendering with Next.js App Router

## Configuration Files

### Backend
- `backend/pyproject.toml`: Project configuration, dependencies, pytest settings
- `backend/app/.env`: Environment variables (not in repo, required for runtime)
- `backend/app/.env.example`: Environment variable template

### Frontend
- `frontend/package.json`: NPM dependencies and Nx scripts
- `frontend/nx.json`: Nx workspace configuration with caching and task orchestration
- `frontend/tsconfig.base.json`: Base TypeScript configuration
- `frontend/apps/chat/tailwind.config.js`: Tailwind CSS configuration
- `frontend/apps/chat/postcss.config.js`: PostCSS configuration
- `frontend/apps/chat/next.config.js`: Next.js configuration
- `frontend/apps/chat/package.json`: App-specific dependencies
- `frontend/apps/chat-e2e/playwright.config.ts`: E2E test configuration
