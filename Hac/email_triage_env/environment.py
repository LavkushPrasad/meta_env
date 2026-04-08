from typing import Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
from openenv import OpenEnv, Observation, Action, Reward
import random
from tasks import TASKS
from graders import GradeEmailTriage, GradeResponseDrafting, GradeEscalation

class EmailState(BaseModel):
    current_email_index: int = 0
    email_queue: list = Field(default_factory=list)
    drafted_responses: dict = Field(default_factory=dict)
    escalation_log: list = Field(default_factory=list)
    priority_assignments: dict = Field(default_factory=dict)
    completed: bool = False

class EmailTriageEnv(OpenEnv):
    def __init__(self, task_name: str = "easy_email_triage"):
        super().__init__()
        self.task_name = task_name
        self.task = TASKS[task_name]
        self.grader = self._get_grader(task_name)
        self.state = EmailState()
        self.current_step = 0
        self.max_steps = self.task.get("max_steps", 20)
        self._load_emails()
    
    def _get_grader(self, task_name: str):
        graders = {
            "easy_email_triage": GradeEmailTriage(),
            "medium_response_drafting": GradeResponseDrafting(),
            "hard_complex_escalation": GradeEscalation()
        }
        return graders[task_name]
    
    def _load_emails(self):
        if self.task_name == "easy_email_triage":
            self.state.email_queue = self.task["emails"]
        elif self.task_name == "medium_response_drafting":
            self.state.email_queue = self.task["emails"]
        else:
            self.state.email_queue = self.task["emails"]
    
    def reset(self) -> Observation:
        self.state = EmailState()
        self.current_step = 0
        self._load_emails()
        return self._get_observation()
    
    def _get_observation(self) -> Observation:
        if self.state.current_email_index >= len(self.state.email_queue):
            return Observation(content={"done": True, "message": "All emails processed"})
        
        email = self.state.email_queue[self.state.current_email_index]
        return Observation(content={
            "email_id": email["id"],
            "from_address": email["from"],
            "subject": email["subject"],
            "body": email["body"][:500],  # truncate for token limits
            "urgency_keywords": self._extract_urgency_keywords(email["body"]),
            "priority_history": self.state.priority_assignments.get(email["id"], []),
            "step": self.current_step,
            "task": self.task_name
        })
    
    def _extract_urgency_keywords(self, text: str) -> list:
        keywords = ["urgent", "asap", "critical", "deadline", "issue", "bug", "complaint"]
        return [kw for kw in keywords if kw in text.lower()]
    
    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict]:
        # Penalize infinite loops
        if self.current_step >= self.max_steps:
            return self._get_observation(), Reward(value=0.0), True, {"error": "max_steps_exceeded"}
        
        email = self.state.email_queue[self.state.current_email_index]
        
        # Process action
        if action.value == 0:  # Low priority
            self.state.priority_assignments[email["id"]] = "low"
            reward_val = self._calculate_reward(email, "low", action)
            self.state.current_email_index += 1
        elif action.value == 1:  # Medium priority
            self.state.priority_assignments[email["id"]] = "medium"
            reward_val = self._calculate_reward(email, "medium", action)
            self.state.current_email_index += 1
        elif action.value == 2:  # High priority
            self.state.priority_assignments[email["id"]] = "high"
            reward_val = self._calculate_reward(email, "high", action)
            self.state.current_email_index += 1
        elif action.value == 3:  # Draft reply
            reward_val = self._calculate_draft_reward(email, action)
            self.state.current_email_index += 1
        elif action.value == 4:  # Escalate
            self.state.escalation_log.append(email["id"])
            reward_val = self._calculate_escalation_reward(email)
            self.state.current_email_index += 1
        elif action.value == 5:  # Archive
            reward_val = 0.3  # Small positive for cleaning up
            self.state.current_email_index += 1
        else:
            reward_val = -0.2  # Penalize invalid actions
        
        self.current_step += 1
        done = self.state.current_email_index >= len(self.state.email_queue) or self.current_step >= self.max_steps
        
        reward_obj = Reward(value=max(0.0, min(1.0, reward_val)))
        info = {"step": self.current_step, "total_emails": len(self.state.email_queue)}
        
        return self._get_observation(), reward_obj, done, info
    
    def _calculate_reward(self, email: dict, assigned_priority: str, action) -> float:
        correct_priority = email.get("expected_priority", "medium")
        
        if assigned_priority == correct_priority:
            return 0.8
        elif (assigned_priority == "high" and correct_priority == "medium") or \
             (assigned_priority == "medium" and correct_priority == "low"):
            return 0.4
        elif assigned_priority == "high" and correct_priority == "low":
            return 0.1
        else:
            return -0.3
    
    def _calculate_draft_reward(self, email: dict, action) -> float:
        # Incremental reward - penalize drafts without actual content
        if hasattr(action, 'metadata') and action.metadata.get("draft_text"):
            return 0.6
        return -0.2
    
    def _calculate_escalation_reward(self, email: dict) -> float:
        if email.get("needs_escalation", False):
            return 0.7
        return -0.5
    
    def state(self) -> Dict[str, Any]:
        return self.state.dict()