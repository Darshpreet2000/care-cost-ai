# main.py
import os
import uuid
import json
import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.apps.app import App
from google.genai import types

from execution_workflow import workflow

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()

medi_app = App(
    name="medi-compare-app",
    root_agent=workflow
)

runner = Runner(
    app=medi_app,
    session_service=session_service
)


# -------------------------------------------------------------------
# Utility Helpers
# -------------------------------------------------------------------

async def get_or_create_session(app_name: str, user_id: str, session_id: str):
    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    if not session:
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )

    return session


def make_id():
    return str(uuid.uuid4())


def get_ids(request: Request):
    user_id = (
        request.headers.get("x-user-id")
        or request.query_params.get("user_id")
        or str(uuid.uuid4())
    )

    session_id = (
        request.headers.get("x-session-id")
        or request.query_params.get("session_id")
        or str(uuid.uuid4())
    )

    return user_id, session_id


def build_payload(event, user_id, session_id, step):
    """
    Converts raw ADK event into structured JSON for UI consumption.
    """
    agent = getattr(event, "author", None)
    event_id = make_id()
    timestamp = datetime.datetime.utcnow().isoformat()

    content_text = None
    tool_call = None
    tool_result = None
    event_type = "message"

    # Handle content parts
    if event.content and event.content.parts:
        texts = []

        for p in event.content.parts:
            if getattr(p, "text", None):
                texts.append(p.text)

            if hasattr(p, "function_call") and p.function_call:
                tool_call = {
                    "name": p.function_call.name,
                    "arguments": p.function_call.args
                }
                event_type = "tool_call"

            if hasattr(p, "function_response") and p.function_response:
                tool_result = p.function_response.response
                event_type = "tool_result"

        if texts:
            content_text = "\n".join(texts)
            event_type = "message"

    # Pause indicator
    if event.actions and getattr(event.actions, "end_of_agent", False):
        event_type = "pause"

    return {
        "agent": agent,
        "type": event_type,
        "content": content_text,
        "tool_call": tool_call,
        "tool_result": tool_result,
        "metadata": {
            "user_id": user_id,
            "session_id": session_id,
            "event_id": event_id,
            "timestamp": timestamp,
            "step": step
        }
    }


# -------------------------------------------------------------------
# Chat Endpoint
# -------------------------------------------------------------------
@app.get("/chat")
async def chat(query: str, request: Request):
    user_id, session_id = get_ids(request)

    # Ensure session exists
    session = await get_or_create_session(
        app_name=medi_app.name,
        user_id=user_id,
        session_id=session_id
    )

    async def stream():
        step = 1

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.UserContent(parts=[types.Part(text=query)])
        ):
            payload = build_payload(event, user_id, session_id, step)

            # Send SSE message
            yield f"data: {json.dumps(payload)}\n\n"

            # Stop early if paused
            if payload["type"] == "pause":
                return
            
            step += 1

        yield "data: [DONE]\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.get("/")
async def root():
    return {"message": "MediCompare backend is running"}


# Dev server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
