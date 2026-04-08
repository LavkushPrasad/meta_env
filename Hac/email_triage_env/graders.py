from typing import Dict, Any

class GradeEmailTriage:
    """Programmatic grader for email triage task - deterministic score 0.0-1.0"""
    
    def grade(self, trajectory: list) -> float:
        correct = 0
        total = 0
        
        for step in trajectory:
            if step.get("action") is not None and step.get("email"):
                expected = step["email"].get("expected_priority")
                assigned = step["action"].get("priority")
                
                if expected and assigned:
                    total += 1
                    if expected == assigned:
                        correct += 1
        
        return correct / total if total > 0 else 0.0

class GradeResponseDrafting:
    """Grades response quality based on keywords and appropriateness"""
    
    def grade(self, trajectory: list) -> float:
        score = 0.0
        total = len([s for s in trajectory if s.get("action", {}).get("type") == "draft"])
        
        for step in trajectory:
            if step.get("action", {}).get("type") == "draft":
                draft = step["action"].get("text", "").lower()
                email = step.get("email", {})
                
                # Check for appropriate response elements
                if "complaint" in email.get("subject", "").lower():
                    if any(word in draft for word in ["apolog", "sorry", "refund"]):
                        score += 0.8
                    else:
                        score += 0.2
                elif "question" in email.get("subject", "").lower():
                    if any(word in draft for word in ["answer", "explain", "help"]):
                        score += 0.7
                    else:
                        score += 0.3
                else:
                    score += 0.5
        
        return min(1.0, score / total) if total > 0 else 0.0

class GradeEscalation:
    """Deterministic grader for escalation decisions"""
    
    def grade(self, trajectory: list) -> float:
        correct_escalations = 0
        total_escalation_decisions = 0
        
        for step in trajectory:
            if step.get("action", {}).get("type") == "escalate":
                total_escalation_decisions += 1
                email = step.get("email", {})
                if email.get("needs_escalation", False):
                    correct_escalations += 1
            elif step.get("email", {}).get("needs_escalation", False):
                total_escalation_decisions += 1  # Should have escalated but didn't
        
        return correct_escalations / total_escalation_decisions if total_escalation_decisions > 0 else 0.0