from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import uvicorn
import os

# Import your environment
from environment import EmailTriageEnv

app = FastAPI(title="Email Triage RL Environment")

# Store environment instances
envs: Dict[str, EmailTriageEnv] = {}

# Request/Response Models
class ResetRequest(BaseModel):
    task_name: str = "easy_email_triage"

class StepRequest(BaseModel):
    action: int = Field(..., ge=0, le=5, description="Action: 0=Low,1=Medium,2=High,3=Draft,4=Escalate,5=Archive")
    session_id: str = "default"

class ResetResponse(BaseModel):
    success: bool
    observation: Dict[str, Any]
    session_id: str

class StepResponse(BaseModel):
    success: bool
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "name": "Email Triage RL Environment",
        "version": "1.0.0",
        "endpoints": {
            "POST /reset": "Initialize environment",
            "POST /step": "Take an action",
            "GET /state": "Get current state",
            "GET /": "Health check"
        }
    }

@app.post("/reset")
async def reset_endpoint(request: ResetRequest = ResetRequest()) -> ResetResponse:
    """Reset the environment to initial state"""
    try:
        session_id = "default"
        
        # Create new environment instance
        env = EmailTriageEnv(task_name=request.task_name)
        envs[session_id] = env
        
        # Get initial observation
        observation = env.reset()
        
        return ResetResponse(
            success=True,
            observation=observation.content if hasattr(observation, 'content') else observation,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")

@app.post("/step")
async def step_endpoint(request: StepRequest) -> StepResponse:
    """Take an action in the environment"""
    try:
        session_id = request.session_id
        
        # Check if environment exists
        if session_id not in envs:
            raise HTTPException(
                status_code=400, 
                detail="Environment not initialized. Call /reset first."
            )
        
        env = envs[session_id]
        
        # Create action object (matches your environment's expected format)
        class Action:
            def __init__(self, value):
                self.value = value
                self.metadata = {}  # For draft text if needed
        
        action = Action(request.action)
        
        # Step the environment
        observation, reward, done, info = env.step(action)
        
        # Extract observation content
        obs_content = observation.content if hasattr(observation, 'content') else observation
        
        return StepResponse(
            success=True,
            observation=obs_content,
            reward=reward.value if hasattr(reward, 'value') else reward,
            done=done,
            info=info
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step failed: {str(e)}")

@app.get("/state")
async def state_endpoint(session_id: str = "default"):
    """Get the current state of the environment"""
    try:
        if session_id not in envs:
            raise HTTPException(
                status_code=400,
                detail="Environment not initialized. Call /reset first."
            )
        
        env = envs[session_id]
        state = env.state()
        
        return JSONResponse(content={
            "success": True,
            "state": state
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get state failed: {str(e)}")

@app.delete("/reset")
async def hard_reset(session_id: str = "default"):
    """Delete environment instance"""
    if session_id in envs:
        del envs[session_id]
    return {"success": True, "message": "Environment cleared"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    print(f"Starting Email Triage Environment Server on port {port}")
    print(f"API Documentation: http://localhost:{port}/docs")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
