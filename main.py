import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from workflow import workflow

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ADK Runner
session_service = InMemorySessionService()
runner = Runner(agent=workflow, session_service=session_service)

# --- API Endpoints ---

@app.get("/workflow/stream")
async def stream_workflow(query: str, request: Request):
    async def event_generator():
        async for event in runner.async_stream_query(
            user_id="user-123",
            message=query
        ):
            if await request.is_disconnected():
                break
            yield f"data: {event.json()}\\n\\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/")
async def root():
    return {"message": "MediCompareAI Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
