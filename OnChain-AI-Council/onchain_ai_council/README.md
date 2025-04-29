# OnChain AI Council

## Overview
This project demonstrates an agentic AI multi-agent system integrated with blockchain governance using smart contracts.

## Features
- Submit proposals via a Streamlit UI
- Agents debate and vote
- Decisions are recorded on-chain

## Setup
1. Run Ganache
2. Deploy contract: `python deploy_contract.py`
3. Start UI: `streamlit run streamlit_app.py`

## Agents
- Obi-Wan (Strategist)
- Yoda (Ethicist)
- Mace Windu (Resource Manager)
- Ahsoka Tano (Risk Analyst)

# A detailed description
The flow will be like below :- 
- User Submit  AI Council debates -- Vote - Blockchain stores votes and decision -- UI will show final Result.

- Step-1 :- User submits the proposal
    - The user opens the streamlit web app
    - They fill out a simple form:-
       -- Proposal Title and Description
    - When they click Submit , a transaction is created.
    - The proposal is sent to the smart contract deployed on Ganache blockchain.
    - After successful submission, a Proposal ID and Blockchain Transaction Hash are shown.

- Step 2:- The system has multiple AI agents:
       - Obi-Wan (Strategist)
       - Yoda (Ethicist)
       - Mace Windu(Resource manager)
       - Ahsoka Tano(Risk Analyst)

      After the proposal is submitted , each agent:-
       1. Reads the title and description
       2. Analyzes the proposal independently based on it's role
       3. Gives it's opinion - Approve or Reject
       4. Generates a small justification log for it's decision

Step 3 :- (Agents Cast Votes - On-chain)
	- After debating , each agent votes:- 
           - vote = Approve or Reject
 	  Each vote is pushed to blockchain using the smart contract's vote function.
 	  Each vote generates separate blockchain transaction with its own TX hash.

Step 4 :- (Finalize the proposal)
	- After all agents have voted:-
    	- The system calls the smart contract's finalizeProposal function.
	-  If majority voted Approve - Proposal gets approved
	- Otherwise - Rejected

Final decision is also recorded on blockchain.
The UI displays the final result to the user.
