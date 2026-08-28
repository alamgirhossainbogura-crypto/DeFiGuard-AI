from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent_runtime.orchestrator import root_agent

APP_NAME = "defiguard_ai"

# Created once at import time and reused across requests - creating a new
# Runner/session per request is wasteful and was flagged as an anti-pattern
# in ADK's own FastAPI integration guidance.
session_service = InMemorySessionService()
runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service,
)


async def run_scan(user_id: str, session_id: str, prompt: str) -> str:
    """Runs the audit agent for a single scan and returns the final text response."""
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text

    return final_text
