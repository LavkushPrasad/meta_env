TASKS = {
    "easy_email_triage": {
        "name": "Email Priority Classification",
        "difficulty": "easy",
        "description": "Classify incoming support emails as low, medium, or high priority",
        "max_steps": 15,
        "emails": [
            {
                "id": 1,
                "from": "user@example.com",
                "subject": "Question about billing",
                "body": "Hi, I have a simple question about my last invoice. Can you explain the charges?",
                "expected_priority": "low",
                "needs_escalation": False
            },
            {
                "id": 2,
                "from": "customer@company.com",
                "subject": "URGENT: System down",
                "body": "Our entire system is down! This is critical for our business operations. Please help ASAP.",
                "expected_priority": "high",
                "needs_escalation": True
            },
            {
                "id": 3,
                "from": "partner@org.com",
                "subject": "Follow up on integration",
                "body": "Just checking in on the API integration timeline. Not urgent.",
                "expected_priority": "low",
                "needs_escalation": False
            },
            {
                "id": 4,
                "from": "manager@internal.com",
                "subject": "Team meeting tomorrow",
                "body": "Reminder: team sync at 10am. Please confirm attendance.",
                "expected_priority": "medium",
                "needs_escalation": False
            }
        ]
    },
    
    "medium_response_drafting": {
        "name": "Response Drafting",
        "difficulty": "medium",
        "description": "Draft appropriate responses to customer queries",
        "max_steps": 20,
        "emails": [
            {
                "id": 1,
                "from": "angry_user@email.com",
                "subject": "Complaint: Product not working",
                "body": "I bought your product and it doesn't work at all. I want a refund immediately.",
                "expected_action": "draft_apology_and_refund",
                "needs_escalation": True
            },
            {
                "id": 2,
                "from": "curious@startup.io",
                "subject": "Pricing question",
                "body": "Do you offer student discounts? I'm building a project for my thesis.",
                "expected_action": "draft_discount_info",
                "needs_escalation": False
            },
            {
                "id": 3,
                "from": "tech@enterprise.com",
                "subject": "API rate limit increase request",
                "body": "We're hitting your rate limits. Can we get a temporary increase?",
                "expected_action": "draft_rate_limit_policy",
                "needs_escalation": False
            }
        ]
    },
    
    "hard_complex_escalation": {
        "name": "Complex Escalation Decision",
        "difficulty": "hard",
        "description": "Decide when to escalate, when to resolve, and when to prioritize",
        "max_steps": 25,
        "emails": [
            {
                "id": 1,
                "from": "legal@customer.com",
                "subject": "Legal complaint: GDPR violation",
                "body": "You are processing my data without consent. Legal action will be taken.",
                "expected_priority": "high",
                "needs_escalation": True
            },
            {
                "id": 2,
                "from": "vip@premium.com",
                "subject": "Executive escalation: Service degradation",
                "body": "Our VP is extremely unhappy with recent performance issues.",
                "expected_priority": "high",
                "needs_escalation": True
            },
            {
                "id": 3,
                "from": "normal@user.net",
                "subject": "Feature request",
                "body": "It would be nice if you added dark mode. Thanks!",
                "expected_priority": "low",
                "needs_escalation": False
            }
        ]
    }
}