import os
import json
from openai import OpenAI
from environment import EmailTriageEnv
from graders import GradeEmailTriage, GradeResponseDrafting, GradeEscalation

# Read API token from environment
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("Please set HF_TOKEN environment variable")

client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key=HF_TOKEN
)

def run_baseline(task_name: str, model: str = "meta-llama/Llama-3.2-3B-Instruct"):
    env = EmailTriageEnv(task_name=task_name)
    obs = env.reset()
    done = False
    trajectory = []
    
    while not done:
        # Simple baseline policy
        email_content = obs.content.get("body", "")
        prompt = f"Classify this email priority (low/medium/high): {email_content[:200]}"
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        
        # Parse action from response
        text = response.choices[0].message.content.lower()
        if "high" in text:
            action = 2
        elif "medium" in text:
            action = 1
        else:
            action = 0
        
        obs, reward, done, info = env.step(action)
        trajectory.append({
            "action": {"value": action, "priority": ["low", "medium", "high"][action]},
            "email": obs.content if hasattr(obs, 'content') else {},
            "reward": reward.value
        })
    
    # Grade trajectory
    if task_name == "easy_email_triage":
        grader = GradeEmailTriage()
    elif task_name == "medium_response_drafting":
        grader = GradeResponseDrafting()
    else:
        grader = GradeEscalation()
    
    final_score = grader.grade(trajectory)
    return final_score

if __name__ == "__main__":
    tasks = ["easy_email_triage", "medium_response_drafting", "hard_complex_escalation"]
    results = {}
    
    for task in tasks:
        print(f"\nRunning baseline on {task}...")
        score = run_baseline(task)
        results[task] = score
        print(f"Score: {score:.3f}")
    
    with open("baseline_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n=== BASELINE PERFORMANCE ===")
    for task, score in results.items():
        print(f"{task}: {score:.3f}")