import random

class Proposal:
    def __init__(self, title, description, patent_matches=None):
        self.title = title
        self.description = description
        self.patent_matches = patent_matches or []

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def analyze_proposal(self, proposal: Proposal):
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
        if any(word in proposal.description.lower() for word in ["scalable", "growth", "long term", "strategic"]):
            return "Approve"
        return "Reject"

    def evaluate_ethics(self, proposal):
        if any(word in proposal.description.lower() for word in ["exploit", "unfair", "harm", "bias", "manipulate"]):
            return "Reject"
        return "Approve"

    def evaluate_resources(self, proposal):
        if any(word in proposal.description.lower() for word in ["expensive", "overbudget", "high cost", "resource intensive"]):
            return "Reject"
        return "Approve"

    def evaluate_risks(self, proposal):
        if any(word in proposal.description.lower() for word in ["volatile", "risky", "uncertain", "unpredictable", "unproven"]):
            return "Reject"
        return "Approve"

    def evaluate_novelty(self, proposal):
        if not proposal.patent_matches:
            return "Approve"
        
        # If top match is highly similar (>80), reject
        if proposal.patent_matches[0]["score"] >= 80:
            return "Reject"
        
        # If top match is moderately similar (50-79), randomly decide
        if 50 <= proposal.patent_matches[0]["score"] < 80:
            return random.choice(["Approve", "Reject"])

        return "Approve"

    def generate_reason(self, proposal, opinion):
        if self.role == "Patent Novelty Evaluator" and proposal.patent_matches:
            best_match = proposal.patent_matches[0]
            return (f"As a {self.role}, I vote to {opinion} because a similar patent exists "
                    f"('{best_match['title']}' with similarity score {best_match['score']}%).")
        return f"As a {self.role}, I vote to {opinion} the proposal '{proposal.title}'."

class Council:
    def __init__(self, agents):
        self.agents = agents

    def debate_and_vote(self, proposal: Proposal):
        debate_logs = []
        votes = {"Approve": 0, "Reject": 0}
        agent_opinions = []

        for agent in self.agents:
            opinion, reason = agent.analyze_proposal(proposal)
            debate_logs.append(f"{agent.name} ({agent.role}): {reason}")
            votes[opinion] += 1
            agent_opinions.append((agent.name, opinion, reason))

        decision = "Approve" if votes["Approve"] > votes["Reject"] else "Reject"
        return debate_logs, votes, decision, agent_opinions
