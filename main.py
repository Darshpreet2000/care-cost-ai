import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events.event import Event
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

# --- API Endpoints ---

@app.get("/api/stream-progress")
async def stream_progress(query: str, request: Request):
    async def event_generator():
        context = InvocationContext()
        context.set_state("user_query", query) # Store the initial user query

        async for event in workflow.run(context):
            if await request.is_disconnected():
                break
            yield f"data: {json.dumps({'agent': event.agent_name, 'message': event.output_value})}\n\n"
            await asyncio.sleep(0.1) # Small delay to simulate processing

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/")
async def root():
    return {"message": "MediCompareAI Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
