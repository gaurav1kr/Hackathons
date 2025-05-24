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
        keywords = ["scalable", "growth", "expansion", "market", "long term"]
        found = any(word in (proposal.title + proposal.description).lower() for word in keywords)
        return "Approve" if found else random.choice(["Approve", "Reject"])

    def evaluate_ethics(self, proposal):
        unethical = ["exploit", "unfair", "harm", "bias", "discriminate"]
        found = any(word in (proposal.title + proposal.description).lower() for word in unethical)
        return "Reject" if found else random.choice(["Approve"] * 3 + ["Reject"])

    def evaluate_resources(self, proposal):
        costly = ["expensive", "overbudget", "high cost", "resource intensive"]
        found = any(word in (proposal.title + proposal.description).lower() for word in costly)
        return "Reject" if found else random.choice(["Approve", "Approve", "Reject"])

    def evaluate_risks(self, proposal):
        risky = ["volatile", "risky", "uncertain", "unpredictable", "unstable"]
        found = any(word in (proposal.title + proposal.description).lower() for word in risky)
        return "Reject" if found else random.choice(["Approve", "Reject"])

    def evaluate_novelty(self, proposal):
        if not proposal.patent_matches:
            return "Approve"
        top_match = proposal.patent_matches[0]
        score = top_match.get("score", 0) if isinstance(top_match, dict) else 0
        return "Reject" if score >= 10 else "Approve"

    def generate_reason(self, proposal, opinion):
        if self.role == "Patent Novelty Evaluator" and proposal.patent_matches:
            best_match = proposal.patent_matches[0]
            title = best_match.get("title", "Unknown")
            score = best_match.get("score", "?")
            return f"As a {self.role}, I vote to {opinion} because similar patent '{title}' scored {score}%."
        return f"As a {self.role}, I vote to {opinion} the proposal '{proposal.title}'."

class Council:
    def __init__(self, agents):
        self.agents = agents

    def debate_and_vote(self, proposal: Proposal):
        debate_logs = []
        votes = {"Approve": 0, "Reject": 0}
        agent_opinions = []
        novelty_rejected = False
        novelty_reason = ""

        for agent in self.agents:
            opinion, reason = agent.analyze_proposal(proposal)
            debate_logs.append(f"{agent.name} ({agent.role}): {reason}")
            votes[opinion] += 1
            agent_opinions.append((agent.name, opinion, reason))

            if agent.role == "Patent Novelty Evaluator" and opinion == "Reject":
                novelty_rejected = True
                novelty_reason = reason

        if novelty_rejected:
            debate_logs.append("⚠️ Council Override: Final decision is ❌ Reject due to novelty conflict.")
            debate_logs.append(f"🧬 Reason: {novelty_reason}")

        decision = "Reject" if novelty_rejected else ("Approve" if votes["Approve"] > votes["Reject"] else "Reject")
        return debate_logs, votes, decision, agent_opinions
