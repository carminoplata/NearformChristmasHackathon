# ElfAgent - AI Christmas Gift Advisor

AI-powered Christmas gift advisor that searches multiple online marketplaces (Amazon, Alibaba) to identify the best deals for Christmas gifts.

## 📚 Documentation

- **[Design Documentation](docs/Design.md)** - System architecture, diagrams, and technical design
- **[TODO & Roadmap](docs/TODO.md)** - Feature roadmap, improvements, and deployment plans
- **[API Reference](backend/API.md)** - Complete API documentation
- **[Backend README](backend/README.md)** - Backend setup and development guide
- **[Frontend README](frontend/README.md)** - Frontend setup and development guide

## Architecture

The project is split into two main parts:

- **Backend**: FastAPI server with Google ADK hierarchical agent system
- **Frontend**: Next.js application with React 19 and Nx monorepo

## 🎥 Demo

Watch Buddy the Christmas Assistant in action:

https://github.com/user-attachments/assets/your-video-id-here

> **Note:** Upload the video `docs/Buddy_ChristmasAssistant.mov` to your GitHub repository, and GitHub will automatically generate a video player. Alternatively, you can host it on YouTube or another platform and embed the link.

**Demo Video:** [docs/Buddy_ChristmasAssistant.mov](docs/Buddy_ChristmasAssistant.mov)

## Features

- 🎄 **Christmas-themed chat interface** with animated snowflakes
- 🛍️ **Multi-marketplace search** across Amazon and Alibaba
- 🔍 **Product feature analysis** via Google Search
- ✅ **User confirmation workflow** before executing searches
- 📊 **Deal aggregation and ranking** by quality and price
- 💬 **Real-time chat** with AI gift advisor
- 🎁 **Product cards** with images, prices, ratings, and direct links
- 📱 **Responsive design** for desktop and mobile
- 🚀 **REST API and WebSocket support**

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** with `uv` package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Node.js 18+** with npm
- **API Keys:**
  - Google API Key (for Gemini LLM and Search)
  - OpenAI API Key (for LiteLLM)
  - RapidAPI Key (for Amazon and Alibaba marketplace data)

### Option 1: Automated Start (Recommended)

**Linux/Mac:**
```bash
./start-dev.sh
```

**Windows:**
```bash
start-dev.bat
```

This will:
1. Start the backend server on `http://localhost:8000`
2. Start the frontend dev server on `http://localhost:4200`

### Option 2: Manual Start

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   uv sync --all-extras
   ```

3. **Configure environment variables:**
   ```bash
   cp app/.env.example app/.env
   ```
   
   Edit `app/.env` and add your API keys:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   RAPIDAPI_KEY=your_rapidapi_key_here
   GOOGLE_MODEL=gemini-1.5-pro
   LLM_MODEL=gpt-4o-mini
   ```

4. **Run the server:**
   ```bash
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend API will be available at `http://localhost:8000`

#### Frontend Setup

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   nx dev chat
   ```
   OR
    ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:4200`

### Accessing the Application

- **Frontend UI:** http://localhost:4200
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🔧 Configuration

### Backend Environment Variables

Create `backend/app/.env` with the following variables:

```env
# Required API Keys
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
RAPIDAPI_KEY=your_rapidapi_key_here

# Model Configuration
GOOGLE_MODEL=gemini-1.5-pro
LLM_MODEL=gpt-4o-mini
```

### Frontend Environment Variables (Optional)

For production deployment, create `frontend/apps/chat/.env.local`:

```env
# Production API URL
NEXT_PUBLIC_API_URL=https://your-production-api.com

# Production WebSocket URL
NEXT_PUBLIC_WS_URL=wss://your-production-api.com
```

**Note:** Development automatically uses `http://localhost:8000` for the API.

## 📖 API Documentation

Once the backend is running, you can access:

- **Interactive API Docs (Swagger):** http://localhost:8000/docs
- **Alternative API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **Detailed API Reference:** [backend/API.md](backend/API.md)

### Key Endpoints

- `POST /api/query` - Process gift search queries
- `GET /health` - Service health status
- `WS /ws/query` - WebSocket streaming (not yet implemented in frontend)

## 📁 Project Structure

```
.
├── docs/                           # Documentation
│   ├── Design.md                   # System architecture and diagrams
│   └── TODO.md                     # Roadmap and improvements
│
├── backend/                        # Python FastAPI backend
│   ├── app/
│   │   ├── elfagent/              # Agent definitions and builders
│   │   │   └── agent.py           # Hierarchical agent system
│   │   ├── tools/                 # External API integrations
│   │   │   ├── awstools.py        # Amazon marketplace API
│   │   │   ├── alibabatools.py    # Alibaba marketplace API
│   │   │   └── agenttools.py      # Agent-specific tools
│   │   ├── utils/                 # Utilities and configuration
│   │   │   ├── utility.py         # Session management, LLM config
│   │   │   └── const.py           # Constants and env vars
│   │   ├── main.py                # FastAPI application entry
│   │   ├── .env                   # Environment variables (not in repo)
│   │   └── .env.example           # Environment template
│   ├── tests/                     # Test suite
│   │   ├── units/                 # Unit tests
│   │   ├── integrations/          # Integration tests
│   │   └── e2e/                   # End-to-end tests
│   ├── pyproject.toml             # Python dependencies
│   ├── uv.lock                    # Dependency lock file
│   ├── API.md                     # API documentation
│   └── README.md                  # Backend guide
│
├── frontend/                      # Next.js frontend (Nx monorepo)
│   ├── apps/
│   │   ├── chat/                  # Main Next.js application
│   │   │   ├── src/
│   │   │   │   ├── app/           # Next.js App Router
│   │   │   │   │   ├── page.tsx   # Main page
│   │   │   │   │   └── layout.tsx # Root layout
│   │   │   │   ├── components/    # React components
│   │   │   │   │   ├── chat_interface.tsx
│   │   │   │   │   ├── chat_message.tsx
│   │   │   │   │   ├── product_card.tsx
│   │   │   │   │   └── snowflakes.tsx
│   │   │   │   └── lib/           # Utilities
│   │   │   │       └── config.ts  # API configuration
│   │   │   ├── public/            # Static assets
│   │   │   │   ├── elf_icon.png
│   │   │   │   └── elf_avatar.png
│   │   │   ├── next.config.js
│   │   │   ├── tailwind.config.js
│   │   │   └── package.json
│   │   └── chat-e2e/              # E2E tests (Playwright)
│   ├── nx.json                    # Nx workspace config
│   ├── package.json               # Root dependencies
│   ├── tsconfig.base.json         # TypeScript config
│   └── README.md                  # Frontend guide
│
├── .kiro/                         # Kiro IDE configuration
│   └── steering/                  # Project documentation
│       ├── product.md             # Product overview
│       ├── structure.md           # Project structure
│       └── tech.md                # Technology stack
│
├── start-dev.sh                   # Linux/Mac startup script
├── start-dev.bat                  # Windows startup script
└── README.md                      # This file
```

## 🛠️ Technology Stack

### Backend
- **Python 3.12+** - Programming language
- **FastAPI** - Modern web framework for APIs
- **Google ADK** - Agent Development Kit for hierarchical AI agents
- **LiteLLM** - Multi-LLM support (OpenAI, Gemini, etc.)
- **Google Gemini** - LLM for agent reasoning
- **aiohttp** - Async HTTP client for external APIs
- **uvicorn** - ASGI server
- **pytest** - Testing framework

### Frontend
- **Next.js 16** - React framework with App Router
- **React 19** - UI library
- **TypeScript 5.9** - Type-safe JavaScript
- **Tailwind CSS 3.4** - Utility-first CSS framework
- **Nx 22.2** - Monorepo build system with intelligent caching
- **Playwright** - E2E testing

### External APIs
- **RapidAPI** - Amazon and Alibaba marketplace data
- **Google Search API** - Product research and feature analysis
- **Google Gemini API** - LLM for AI agents
- **OpenAI API** - Alternative LLM via LiteLLM

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/units/tools/test_awstools.py

# Run integration tests
uv run pytest tests/integrations/
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
nx test chat

# Run E2E tests
nx e2e chat-e2e

# Run tests in watch mode
nx test chat --watch
```

## 💻 Development

### Development Workflow

1. **Backend** runs on `http://localhost:8000` with hot-reload
2. **Frontend** runs on `http://localhost:4200` with hot-reload
3. Frontend makes API calls to backend via configured endpoints
4. Both support live code changes without restart

### Common Commands

**Backend:**
```bash
cd backend

# Install dependencies
uv sync --all-extras

# Run development server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
uv run pytest

# Format code
uv run black app/

# Type checking
uv run mypy app/
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Run development server
nx dev chat

# Build for production
nx build chat

# Lint code
nx lint chat

# Format code
npx prettier --write "apps/chat/src/**/*.{ts,tsx}"

# Show dependency graph
nx graph
```

### Code Style

- **Backend:** Follow PEP 8, use Black for formatting
- **Frontend:** Follow Airbnb style guide, use Prettier for formatting
- **Commits:** Use conventional commits (feat:, fix:, docs:, etc.)

## 🌍 Target Market

Currently optimized for the **Italian market**:
- Locale: IT
- Currency: EUR (€)
- Language: Italian
- Marketplaces: Amazon.it, Alibaba (IT)

See [docs/TODO.md](docs/TODO.md) for multi-language support roadmap.

## 🚀 Deployment

### Development
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:4200`

### Production Deployment Options

1. **AWS** (Recommended)
   - Backend: ECS Fargate or EC2
   - Frontend: Vercel or AWS Amplify
   - Database: RDS PostgreSQL
   - Cache: ElastiCache Redis
   - See [docs/TODO.md#cloud-deployment](docs/TODO.md#cloud-deployment) for detailed guide

2. **Google Cloud Platform**
   - Backend: Cloud Run or Compute Engine
   - Frontend: Vercel or Firebase Hosting
   - Database: Cloud SQL
   - Cache: Memorystore

3. **Docker (Self-Hosted)**
   - Use `docker-compose.yml` (to be created)
   - Includes backend, frontend, PostgreSQL, Redis

For detailed deployment instructions, see [docs/TODO.md](docs/TODO.md).

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [docs/TODO.md](docs/TODO.md) for the roadmap and areas needing contribution.

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Google ADK** - Agent Development Kit
- **FastAPI** - Modern Python web framework
- **Next.js** - React framework
- **Nx** - Monorepo build system
- **RapidAPI** - Marketplace data APIs

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Happy Gift Shopping! 🎄🎁**
