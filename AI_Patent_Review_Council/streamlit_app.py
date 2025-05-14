import streamlit as st
from web3 import Web3
import json
import tempfile
from multiagent import Council, Agent, Proposal
from patent_search import search_google_patents

# === Streamlit Page Config ===
st.set_page_config(page_title="AI Patent Review Council", layout="wide")

# === Web3 and Contract Setup ===
GANACHE_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "0x8Cf36E764C44b2404Cae60A3d231eDA3408f4914"  # Update to your contract address

# Load ABI from file
with open("dao_contract_abi.json") as f:
    ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not web3.is_connected():
    st.error("Unable to connect to Ganache.")
    st.stop()

web3.eth.default_account = web3.eth.accounts[0]
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# === AI Council Agents ===
agents = [
    Agent("StratX", "Strategic Analyst"),
    Agent("Ethos", "Ethics Reviewer"),
    Agent("Resourcia", "Resource Analyst"),
    Agent("Riskon", "Risk Evaluator"),
    Agent("Novexa", "Patent Novelty Evaluator")
]
council = Council(agents)

# === Streamlit UI ===
st.title("🏛️ AI Patent Review Council")
st.write("Submit a patent proposal. Let the AI agents analyze and cast their blockchain-backed decisions.")

# === Proposal Input Form ===
with st.form("proposal_form"):
    title = st.text_input("📌 Proposal Title")
    description = st.text_area("📝 Proposal Description")
    submit_button = st.form_submit_button("Submit Proposal")

if submit_button:
    if not title or not description:
        st.warning("Please fill in both title and description.")
        st.stop()

    # === Patent Novelty Search ===
    st.subheader("🔎 Google Patent Search")
    st.info("Searching Google Patents...")
    matches, novelty_score, error = search_google_patents(title, description)
    if error:
        st.error(error)
        matches = []

    if matches:
        st.success("Top matching patents:")
        for entry in matches:
            st.markdown(f"- [{entry['title']}]({entry['url']}) - Similarity: {entry['score']}%")
    else:
        st.info("No matching patents found.")

    # === Submit to Blockchain ===
    st.subheader("📡 Submitting to Blockchain...")
    tx_hash = contract.functions.submitProposal(title, description).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    proposal_id = contract.functions.nextProposalId().call() - 1

    st.success(f"✅ Proposal submitted! ID: {proposal_id}")
    st.caption(f"Blockchain TX Hash: {receipt.transactionHash.hex()}")

    # === AI Council Analysis ===
    st.subheader("🧠 AI Council Analysis")
    proposal_obj = Proposal(title, description, patent_matches=matches)
    debate_logs, votes, decision, agent_opinions = council.debate_and_vote(proposal_obj)

    for log in debate_logs:
        st.write(log)

    # === Downloadable Logs ===
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as f:
        for log in debate_logs:
            f.write(log + "\n")
        if matches:
            f.write("\n\n=== Related Patents ===\n")
            for entry in matches:
                f.write(f"{entry['title']} ({entry['score']}%): {entry['url']}\n")
        temp_path = f.name

    with open(temp_path, "rb") as f:
        st.download_button("📥 Download AI Council Logs", f, file_name="council_log.txt")

    # === On-Chain Voting by Agents ===
    st.subheader("🗳️ On-Chain Voting")
    for agent_name, opinion, _ in agent_opinions:
        approve = (opinion == "Approve")
        tx_vote = contract.functions.vote(proposal_id, agent_name, approve).transact()
        vote_receipt = web3.eth.wait_for_transaction_receipt(tx_vote)
        st.write(f"{agent_name} voted {'✅ Approve' if approve else '❌ Reject'} (TX: {vote_receipt.transactionHash.hex()})")

    # === Finalize and Decision ===
    tx_finalize = contract.functions.finalizeProposal(proposal_id).transact()
    finalize_receipt = web3.eth.wait_for_transaction_receipt(tx_finalize)
    st.success(f"🏁 Final Decision: {decision}")
    st.caption(f"Finalization TX: {finalize_receipt.transactionHash.hex()}")

    st.balloons()
