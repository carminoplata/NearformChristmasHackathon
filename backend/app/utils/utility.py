import os
import logging
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from google.adk.models.google_llm import Gemini

logger = logging.getLogger("uvicorn.error")



def configure_retry():
    retry_config = types.HttpRetryOptions(
        attempts=5,            # Maximum number of retry attempts
        exp_base=7,            # Exponential backoff multiplier (delay grows: 1s, 7s, 49s...)
        initial_delay=1,       # Initial delay before first retry (in seconds)
        http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
    )
    logger.info("✅ Retry configuration created")
    return retry_config

async def run_session(runner: Runner,
                      session_svc: InMemorySessionService, 
                      user_id: str,
                      user_queries: list[str],
                      session_name: str="default"):
    logger.info(f"### SESSION: {session_name.upper()}")
    app_name = runner.app_name
    final_response = {"products": [], "message": "No products found"}
    try:
        session = await session_svc.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_name)
    except:
        session = await session_svc.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_name
        )
    for query in user_queries:
        logger.info(f"User > {query}")

        query = types.Content(role="user", 
                              parts=[types.Part(text=query)])
        
        async for event in runner.run_async(
            user_id=user_id, session_id=session.id,
            new_message=query):
            if event.content and event.content.parts:
                if event.content.parts[0].text != "None" and \
                    event.content.parts[0].text:
                    logger.info(f"Agent > {event.content.parts[0].text}")
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
                break
        return final_response


# gemini-1.5-pro FULL RESOURCES Used
gemini_model = os.getenv("GOOGLE_MODEL", "")
pro_model = os.getenv("LLM_MODEL", "")
google_model = Gemini(model=gemini_model,
                 retry_options=configure_retry())

llm_model = LiteLlm(model=pro_model)


