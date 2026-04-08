# Email Triage & Customer Support RL Environment

## Overview
Real-world simulation of email triage and customer support tasks that human agents perform daily. Agents must prioritize, draft responses, and decide when to escalate issues.

## Motivation
Customer support consumes billions of human hours annually. This environment enables RL agents to learn efficient triage policies that reduce response times and improve customer satisfaction.

## Action Space (6 discrete actions)
- 0: Mark Low Priority
- 1: Mark Medium Priority  
- 2: Mark High Priority
- 3: Draft Reply
- 4: Escalate
- 5: Archive

## Observation Space
Dictionary containing:
- email_id, from_address, subject, body
- urgency_keywords (extracted)
- priority_history
- current_step, task_name

## Tasks

### Easy: Email Priority Classification
Classify emails as low/medium/high priority based on urgency.
- **Grader**: Exact match accuracy
- **Expected baseline**: ~0.6-0.7

### Medium: Response Drafting  
Draft appropriate customer responses with correct tone and information.
- **Grader**: Keyword matching + appropriateness
- **Expected baseline**: ~0.4-0.5

### Hard: Complex Escalation Decision
Decide when to escalate legal/complaint issues vs. resolve directly.
- **Grader**: Correct escalation rate
- **Expected baseline**: ~0.5-0.6

## Baseline Performance (Llama-3.2-3B)
- Easy task: 0.625
- Medium task: 0.433
- Hard task: 0.500

## Setup & Usage

```bash
# Build container
docker build -t email-triage-env .

# Run with Hugging Face token
docker run -e HF_TOKEN="your_token_here" email-triage-env

# Validate OpenEnv compliance
openenv validate .
