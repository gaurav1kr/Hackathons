# multiagent.py

import random

class Proposal:
    def __init__(self, title, description):
        self.title = title
        self.description = description

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def analyze_proposal(self, proposal):
        if self.role == "Strategic Analyst":
            opinion = self.evaluate_strategy(proposal)
        elif self.role == "Ethics Reviewer":
            opinion = self.evaluate_ethics(proposal)
        elif self.role == "Resource Analyst":
            opinion = self.evaluate_resources(proposal)
        elif self.role == "Risk Evaluator":
            opinion = self.evaluate_risks(proposal)
        elif self.role == "Patent Novelty Evaluator":
            opinion = self.evaluate_novelty(proposal)
        else:
            opinion = random.choice(["Approve", "Reject"])

        reason = self.generate_reason(proposal, opinion)
        return opinion, reason

    def evaluate_strategy(self, proposal):
        keywords = ["long term", "scale", "expand", "market"]
        return "Approve" if any(word in proposal.description.lower() for word in keywords) else "Reject"

    def evaluate_ethics(self, proposal):
        unethical = ["exploit", "cheat", "bias", "harm"]
        return "Reject" if any(word in proposal.description.lower() for word in unethical) else "Approve"

    def evaluate_resources(self, proposal):
        red_flags = ["expensive", "overbudget", "high cost"]
        return "Reject" if any(word in proposal.description.lower() for word in red_flags) else "Approve"

    def evaluate_risks(self, proposal):
        risk_terms = ["volatile", "risky", "uncertain", "unpredictable"]
        return "Reject" if any(word in proposal.description.lower() for word in risk_terms) else "Approve"

    def evaluate_novelty(self, proposal):
        # Placeholder logic; real logic should include web search or patent API check
        generic_terms = ["common", "standard", "existing"]
        return "Reject" if any(word in proposal.description.lower() for word in generic_terms) else "Approve"

    def generate_reason(self, proposal, opinion):
        return f"As a {self.role}, I vote to {opinion} the proposal '{proposal.title}'."

class Council:
    def __init__(self, agents):
        self.agents = agents

    def debate_and_vote(self, proposal):
        debate_logs = []
        votes = {"Approve": 0, "Reject": 0}
        agent_opinions = []

        for agent in self.agents:
            opinion, reason = agent.analyze_proposal(proposal)
            debate_logs.append(f"{agent.name} ({agent.role}): {reason}")
            votes[opinion] += 1
            agent_opinions.append((agent, opinion, reason))  # Include agent for downstream use

        decision = "Approve" if votes["Approve"] > votes["Reject"] else "Reject"
        return debate_logs, votes, decision, agent_opinions
