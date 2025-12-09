import os
import uuid
import logging
import json

from contextlib import asynccontextmanager
from typing import Optional

from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google.adk.apps import App, ResumabilityConfig
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.elfagent import root_agent
from app.utils import run_session



# Global state
session_service: Optional[InMemorySessionService] = None
runner: Optional[Runner] = None
#elf_app: Optional[App] = None

logger = logging.getLogger("uvicorn.info")

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Initialize app on startup"""
    global session_service, runner, root_agent
    
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    if not os.getenv("OPENAI_API_KEY"):
       raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    if not os.getenv("LLM_MODEL"):
       raise ValueError("LLM_MODEL not found in environment variables")
    
    if not os.getenv("RAPIDAPI_KEY"):
        raise ValueError("RAPIDAPI_KEY not found in environment variables")
    
    #elf_app = App(
    #    name="elfagent",
    #    root_agent=root_agent,
    #    resumability_config=ResumabilityConfig(is_resumable=True)
    #)
    
    session_service = InMemorySessionService()
    runner = Runner(app_name="elfagent", agent=root_agent, session_service=session_service)
    
    logger.info("✅ ElfAgent API initialized")
    yield
    
    logger.info("🛑 Shutting down ElfAgent API")


app = FastAPI(
    title="ElfAgent API",
    description="AI-powered Christmas gift advisor API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Vite/React dev server
        "http://localhost:4200",  # Nx dev server (default)
        "http://localhost:5173",  # Alternative Vite port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    session_id: str
    user_id: str
    response: str
    status: str


class SessionInfo(BaseModel):
    session_id: str
    user_id: str
    app_name: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "ElfAgent API",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "runner_initialized": runner is not None,
        "session_service_initialized": session_service is not None
    }


@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a gift search query"""
    
    if not runner or not session_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    user_id = request.user_id or str(uuid.uuid4())
    session_id = request.session_id or str(uuid.uuid4())
    
    logger.info(f"Processing query for user_id={user_id}, session_id={session_id}, model={runner.agent.model}")
    try:
        response = await run_session(runner, session_service, user_id, [request.query], session_id)

        return QueryResponse(
            session_id=session_id,
            user_id=user_id,
            response=response,
            status="completed"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.websocket("/ws/query")
async def websocket_query(websocket: WebSocket):
    """WebSocket endpoint for streaming responses"""
    await websocket.accept()
    
    if not runner or not session_service:
        await websocket.send_json({"error": "Service not initialized"})
        await websocket.close()
        return
    
    try:
        # Receive initial connection data
        data = await websocket.receive_json()
        user_id = data.get("user_id", str(uuid.uuid4()))
        session_id = data.get("session_id", str(uuid.uuid4()))
        
        # Send session info
        await websocket.send_json({
            "type": "session_info",
            "user_id": user_id,
            "session_id": session_id
        })
        
        # Get or create session
        try:
            session = await session_service.create_session(
                app_name=elf_app.name,
                user_id=user_id,
                session_id=session_id
            )
        except:
            session = await session_service.get_session(
                app_name=elf_app.name,
                user_id=user_id,
                session_id=session_id
            )
        
        # Listen for queries
        while True:
            data = await websocket.receive_json()
            query = data.get("query")
            
            if not query:
                await websocket.send_json({"error": "No query provided"})
                continue
            
            # Process query and stream responses
            query_content = types.Content(
                role="user",
                parts=[types.Part(text=query)]
            )
            
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session.id,
                new_message=query_content
            ):
                if event.content and event.content.parts:
                    if event.content.parts[0].text and event.content.parts[0].text != "None":
                        await websocket.send_json({
                            "type": "response",
                            "content": event.content.parts[0].text
                        })
            
            await websocket.send_json({"type": "complete"})
    
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()


@app.get("/api/sessions/{user_id}")
async def get_user_sessions(user_id: str):
    """Get all sessions for a user"""
    if not session_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        sessions = await session_service.list_sessions(
            app_name=elf_app.name,
            user_id=user_id
        )
        return {"user_id": user_id, "sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
