from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from environment import EmailTriageEnv
import uvicorn
import os

app = FastAPI(title="Email Triage RL Environment")

# Store environment instances per session (simplified)
envs = {}

class ResetRequest(BaseModel):
    task_name: str = "easy_email_triage"

class ActionRequest(BaseModel):
    action: int
    session_id: str = "default"

@app.post("/reset")
async def reset_endpoint(request: ResetRequest = None):
    task_name = request.task_name if request else "easy_email_triage"
    session_id = "default"
    
    try:
        env = EmailTriageEnv(task_name=task_name)
        envs[session_id] = env
        observation = env.reset()
        
        return {
            "status": "success",
            "observation": observation.content,
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/step")
async def step_endpoint(request: ActionRequest):
    session_id = request.session_id
    action_value = request.action
    
    if session_id not in envs:
        raise HTTPException(status_code=404, detail="Environment not found. Call /reset first.")
    
    env = envs[session_id]
    
    # Convert action value to Action object (adjust based on your Action class)
    from openenv import Action
    action = Action(value=action_value)
    
    observation, reward, done, info = env.step(action)
    
    return {
        "observation": observation.content,
        "reward": reward.value,
        "done": done,
        "info": info
    }

@app.get("/state")
async def state_endpoint(session_id: str = "default"):
    if session_id not in envs:
        raise HTTPException(status_code=404, detail="Environment not found")
    
    state = envs[session_id].state()
    return {"state": state}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)