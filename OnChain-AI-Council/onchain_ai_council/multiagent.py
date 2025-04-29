# multi_agent.py

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
        # Each agent has different focus
        if self.role == "Strategist":
            opinion = self.evaluate_strategy(proposal)
        elif self.role == "Ethicist":
            opinion = self.evaluate_ethics(proposal)
        elif self.role == "Resource Manager":
            opinion = self.evaluate_resources(proposal)
        elif self.role == "Risk Analyst":
            opinion = self.evaluate_risks(proposal)
        else:
            opinion = random.choice(["Approve", "Reject"])
        
        reason = self.generate_reason(proposal, opinion)
        return opinion, reason

    def evaluate_strategy(self, proposal):
        keywords = ["long term", "growth", "scale", "expansion"]
        return "Approve" if any(word in proposal.description.lower() for word in keywords) else "Reject"

    def evaluate_ethics(self, proposal):
        unethical_words = ["exploit", "unfair", "harm", "cheat"]
        return "Reject" if any(word in proposal.description.lower() for word in unethical_words) else "Approve"

    def evaluate_resources(self, proposal):
        costly_words = ["expensive", "high cost", "overbudget"]
        return "Reject" if any(word in proposal.description.lower() for word in costly_words) else "Approve"

    def evaluate_risks(self, proposal):
        risky_words = ["risk", "uncertain", "volatile", "unpredictable"]
        return "Reject" if any(word in proposal.description.lower() for word in risky_words) else "Approve"

    def generate_reason(self, proposal, opinion):
        return f"As a {self.role}, I vote to {opinion} the proposal '{proposal.title}'."

class Council:
    def __init__(self, agents):
        self.agents = agents

    def debate_and_vote(self, proposal):
        debate_logs = []
        votes = {"Approve": 0, "Reject": 0}

        for agent in self.agents:
            opinion, reason = agent.analyze_proposal(proposal)
            debate_logs.append(f"{agent.name} ({agent.role}): {reason}")
            votes[opinion] += 1

        decision = "Approve" if votes["Approve"] > votes["Reject"] else "Reject"
        return debate_logs, votes, decision

# Example usage
if __name__ == "__main__":
    agents = [
        Agent("Obi-Wan", "Strategist"),
        Agent("Yoda", "Ethicist"),
        Agent("Mace Windu", "Resource Manager"),
        Agent("Ahsoka Tano", "Risk Analyst")
    ]

    council = Council(agents)

    # Example Proposal
    proposal = Proposal(
        title="Expand Operations to Outer Rim Territories",
        description="This project focuses on long term expansion and growth into new markets despite volatile conditions."
    )

    debate_logs, votes, final_decision = council.debate_and_vote(proposal)

    print("\n=== Debate Logs ===")
    for log in debate_logs:
        print(log)

    print("\n=== Vote Summary ===")
    print(votes)

    print("\n=== Final Decision ===")
    print(final_decision)
