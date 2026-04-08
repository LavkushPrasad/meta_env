from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from environment import EmailTriageEnv
import uvicorn
import os
import json

app = FastAPI(title="Email Triage RL Environment")

# Store environment instances
envs = {}

class ResetRequest(BaseModel):
    task_name: str = "easy_email_triage"

class StepRequest(BaseModel):
    action: int
    session_id: str = "default"

@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "Email Triage RL Environment is live",
        "endpoints": ["/reset (POST)", "/step (POST)", "/state (GET)"]
    }

@app.post("/reset")
async def reset_endpoint(request: ResetRequest = None):
    try:
        task_name = request.task_name if request else "easy_email_triage"
        session_id = "default"
        
        env = EmailTriageEnv(task_name=task_name)
        envs[session_id] = env
        observation = env.reset()
        
        return JSONResponse(content={
            "success": True,
            "observation": observation.content,
            "session_id": session_id
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/step")
async def step_endpoint(request: StepRequest):
    session_id = request.session_id
    
    if session_id not in envs:
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": "Environment not found. Call /reset first."}
        )
    
    env = envs[session_id]
    
    # Create action object
    class Action:
        def __init__(self, value):
            self.value = value
    
    action = Action(request.action)
    observation, reward, done, info = env.step(action)
    
    return JSONResponse(content={
        "success": True,
        "observation": observation.content,
        "reward": reward.value,
        "done": done,
        "info": info
    })

@app.get("/state")
async def state_endpoint(session_id: str = "default"):
    if session_id not in envs:
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": "Environment not found"}
        )
    
    state = envs[session_id].state()
    return JSONResponse(content={"success": True, "state": state})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
