# streamlit_app.py

import streamlit as st
from multiagent import Council, Agent, Proposal
from web3 import Web3

# === CONFIG ===
GANACHE_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "0x05609B47FDbee3a1778AD4332000A4b5f6151f11"

# ABI of DAOCouncil Contract
ABI = [
    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "proposalId", "type": "uint256"}, {"indexed": False, "internalType": "enum DAOCouncil.Decision", "name": "decision", "type": "uint8"}], "name": "Finalized", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "proposalId", "type": "uint256"}, {"indexed": False, "internalType": "string", "name": "title", "type": "string"}], "name": "ProposalSubmitted", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "proposalId", "type": "uint256"}, {"indexed": False, "internalType": "string", "name": "voter", "type": "string"}, {"indexed": False, "internalType": "bool", "name": "approve", "type": "bool"}], "name": "Voted", "type": "event"},
    {"inputs": [{"internalType": "uint256", "name": "_proposalId", "type": "uint256"}], "name": "finalizeProposal", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_proposalId", "type": "uint256"}], "name": "getProposal", "outputs": [{"components": [{"internalType": "uint256", "name": "id", "type": "uint256"}, {"internalType": "string", "name": "title", "type": "string"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "uint256", "name": "votesApprove", "type": "uint256"}, {"internalType": "uint256", "name": "votesReject", "type": "uint256"}, {"internalType": "enum DAOCouncil.Decision", "name": "finalDecision", "type": "uint8"}], "internalType": "struct DAOCouncil.Proposal", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "nextProposalId", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "proposals", "outputs": [{"internalType": "uint256", "name": "id", "type": "uint256"}, {"internalType": "string", "name": "title", "type": "string"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "uint256", "name": "votesApprove", "type": "uint256"}, {"internalType": "uint256", "name": "votesReject", "type": "uint256"}, {"internalType": "enum DAOCouncil.Decision", "name": "finalDecision", "type": "uint8"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "string", "name": "_title", "type": "string"}, {"internalType": "string", "name": "_description", "type": "string"}], "name": "submitProposal", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_proposalId", "type": "uint256"}, {"internalType": "string", "name": "_voterName", "type": "string"}, {"internalType": "bool", "name": "_approve", "type": "bool"}], "name": "vote", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]

# === INIT Web3 ===
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not web3.is_connected():
    st.error("Cannot connect to Ganache blockchain. Please start Ganache!")
    st.stop()

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
web3.eth.default_account = web3.eth.accounts[0]

# === INIT Agents ===
agents = [
    Agent("Obi-Wan", "Strategist"),
    Agent("Yoda", "Ethicist"),
    Agent("Mace Windu", "Resource Manager"),
    Agent("Ahsoka Tano", "Risk Analyst")
]
council = Council(agents)

# === Streamlit UI ===
st.set_page_config(page_title="OnChain AI Council", layout="wide")
st.title("🏛️ OnChain Assembly: Autonomous AI Council")

st.write("Submit a proposal. Let the AI Council debate, vote, and push the decision to blockchain!")

st.divider()

# === Proposal Submission ===
with st.form("proposal_form"):
    title = st.text_input("Proposal Title")
    description = st.text_area("Proposal Description")
    submit_button = st.form_submit_button("Submit Proposal")

if submit_button:
    if not title or not description:
        st.warning("Please fill in both title and description.")
    else:
        # Submit proposal onchain
        tx_submit = contract.functions.submitProposal(title, description).transact()
        receipt_submit = web3.eth.wait_for_transaction_receipt(tx_submit)
        proposal_id = contract.functions.nextProposalId().call() - 1
        
        st.success(f"✅ Proposal submitted successfully! Proposal ID: {proposal_id}")
        st.info(f"Blockchain TX Hash: {receipt_submit.transactionHash.hex()}")

        # AI Council Debate
        st.subheader("🧠 Council Debate")
        proposal_obj = Proposal(title, description)
        debate_logs, votes, decision = council.debate_and_vote(proposal_obj)

        for log in debate_logs:
            st.write(log)

        # Voting Onchain
        st.subheader("🗳️ Council Voting (OnChain)")

        for agent in agents:
            opinion, _ = agent.analyze_proposal(proposal_obj)
            approve = True if opinion == "Approve" else False
            tx_vote = contract.functions.vote(proposal_id, agent.name, approve).transact()
            receipt_vote = web3.eth.wait_for_transaction_receipt(tx_vote)
            st.write(f"{agent.name} voted {'✅ Approve' if approve else '❌ Reject'} (TX Hash: {receipt_vote.transactionHash.hex()})")

        # Finalize Proposal
        tx_finalize = contract.functions.finalizeProposal(proposal_id).transact()
        receipt_finalize = web3.eth.wait_for_transaction_receipt(tx_finalize)
        st.success(f"🏛️ Final decision: {decision}")
        st.info(f"Blockchain TX Hash: {receipt_finalize.transactionHash.hex()}")

        st.balloons()


