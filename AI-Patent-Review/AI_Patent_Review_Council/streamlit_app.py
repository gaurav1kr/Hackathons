import streamlit as st
from web3 import Web3
import json
from multiagent import Agent, Council, Proposal

# === Streamlit Config ===
st.set_page_config(page_title="AI Patent Review Council", layout="wide")
st.title("🤖 AI Patent Review Council")

# === Blockchain Connection Setup ===
GANACHE_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "0x1b1f5110a396DE7a231243A16eF916db7550CD6E"  # Replace with actual deployed address

# Load ABI
with open("dao_contract_abi.json") as f:
    ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if not web3.is_connected():
    st.error("❌ Cannot connect to Ganache. Please ensure it's running.")
    st.stop()

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
web3.eth.default_account = web3.eth.accounts[0]

# === Define AI Council ===
agents = [
    Agent("StratX", "Strategic Analyst"),
    Agent("Ethos", "Ethics Reviewer"),
    Agent("Resourcia", "Resource Analyst"),
    Agent("Riskon", "Risk Evaluator"),
    Agent("Novexa", "Patent Novelty Evaluator")
]
council = Council(agents)

# === UI Form to Submit Proposal ===
st.subheader("📨 Submit a Proposal for Review")
with st.form("submit_proposal"):
    title = st.text_input("Proposal Title")
    description = st.text_area("Proposal Description")
    submit = st.form_submit_button("Submit to Council")

if submit:
    if not title or not description:
        st.warning("Please provide both title and description.")
        st.stop()

    st.info("📡 Submitting to Blockchain...")

    try:
        tx_submit = contract.functions.submitProposal(title, description).transact()
        receipt = web3.eth.wait_for_transaction_receipt(tx_submit)
        proposal_id = contract.functions.nextProposalId().call() - 1
    except Exception as e:
        st.error(f"❌ Error during blockchain submission: {e}")
        st.stop()

    st.success(f"✅ Proposal submitted! ID: {proposal_id}")
    st.info(f"Blockchain TX Hash: {receipt.transactionHash.hex()}")

    # === AI Council Debate & Decision ===
    st.subheader("🧠 AI Council Analysis")
    proposal_obj = Proposal(title, description)
    debate_logs, votes, decision, agent_opinions = council.debate_and_vote(proposal_obj)

    for log in debate_logs:
        st.write(log)

    # === On-Chain Voting by AI Agents ===
    st.subheader("🗳️ On-Chain Voting")

    for agent, opinion, _ in agent_opinions:
        try:
            tx_vote = contract.functions.vote(proposal_id, agent.name, opinion == "Approve").transact()
            vote_receipt = web3.eth.wait_for_transaction_receipt(tx_vote)
            st.write(f"{agent.name} voted {'✅ Approve' if opinion == 'Approve' else '❌ Reject'} (TX: {vote_receipt.transactionHash.hex()})")
        except Exception as e:
            st.error(f"{agent.name} vote failed: {e}")

    # === Finalize Proposal ===
    try:
        tx_finalize = contract.functions.finalizeProposal(proposal_id).transact()
        finalize_receipt = web3.eth.wait_for_transaction_receipt(tx_finalize)
        st.subheader("📜 Final Decision")
        st.success(f"🏛️ Final Decision: {decision}")
        st.info(f"Blockchain TX Hash: {finalize_receipt.transactionHash.hex()}")
        st.balloons()
    except Exception as e:
        st.error(f"❌ Error during finalization: {e}")
