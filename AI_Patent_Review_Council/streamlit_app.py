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
CONTRACT_ADDRESS = "0x9AfB432f774E84F9D6253Fc829262E8D070Bb781"  # Replace with your deployed contract address

# Load ABI from file
with open("dao_contract_abi.json") as f:
    ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not web3.is_connected():
    st.error("Unable to connect to Ganache.")
    st.stop()

web3.eth.default_account = web3.eth.accounts[0]
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# === Agents ===
agents = [
    Agent("StratX", "Strategic Analyst"),
    Agent("Ethos", "Ethics Reviewer"),
    Agent("Resourcia", "Resource Analyst"),
    Agent("Riskon", "Risk Evaluator"),
    Agent("Novexa", "Patent Novelty Evaluator")
]
council = Council(agents)

# === UI ===
st.title("\U0001F3DB\uFE0F AI Patent Review Council")
st.write("Submit a patent proposal and let the AI Council review and vote on it, backed by blockchain.")

with st.form("proposal_form"):
    title = st.text_input("Proposal Title")
    description = st.text_area("Proposal Description")
    submit_button = st.form_submit_button("Submit Proposal")

if submit_button:
    if not title or not description:
        st.warning("Please enter both title and description.")
        st.stop()

    # === Patent Search ===
    st.subheader("\U0001F50E Google Patent Search")
    st.write("Searching Google Patents...")
    matches, match_count, error = search_google_patents(title, description)

    if error:
        st.error(f"\u274C Search Error: {error}")
    elif match_count == 0:
        st.info("\u2139\uFE0F No matching patents found.")
    else:
        st.success(f"\u2705 Found {match_count} potential match(es):")
        top_score = matches[0]['score'] if matches and isinstance(matches[0], dict) and 'score' in matches[0] else 0
        st.markdown(f"\U0001F4A1 Top Match Score: {top_score}%")
        for match in matches:
            st.markdown(f"- **{match['title']}** — \U0001F50D Similarity Score: {match['score']}%")

    # === Submit to Blockchain ===
    st.subheader("\U0001F4F1 Submitting to Blockchain...")
    tx_hash = contract.functions.submitProposal(title, description).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    proposal_id = contract.functions.nextProposalId().call() - 1

    st.success(f"\u2705 Proposal submitted! ID: {proposal_id}")
    st.caption(f"Blockchain TX Hash: {receipt.transactionHash.hex()}")

    # === AI Analysis ===
    st.subheader("\U0001F9E0 AI Council Analysis")
    proposal_obj = Proposal(title, description, patent_matches=matches)
    debate_logs, votes, decision, agent_opinions = council.debate_and_vote(proposal_obj)

    for log in debate_logs:
        st.write(log)

    # Check override by novelty agent
    novelty_override = any(agent.name == "Novexa" and opinion == "Reject" for agent, (name, opinion, reason) in zip(agents, agent_opinions))
    if novelty_override:
        decision = "Reject"
        novelty_reason = next(reason for (name, opinion, reason) in agent_opinions if name == "Novexa")
        st.warning("\u26A0\uFE0F Council Override: Final decision is ❌ Reject due to novelty conflict.")
        st.caption(f"\U0001F9EC Reason: {novelty_reason}")

    # === Download Logs ===
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt", encoding="utf-8") as f:
        for log in debate_logs:
            f.write(log + "\n")
        if matches:
            f.write("\n\n=== Related Patents ===\n")
            for m in matches:
                f.write(f"{m['title']} - {m['url']}\n")
        temp_path = f.name

    with open(temp_path, "rb") as file:
        st.download_button("\U0001F4E5 Download Debate Logs", file, file_name="council_debate.txt", mime="text/plain")

    # === Voting On-chain ===
    st.subheader("\U0001F5F3\uFE0F On-Chain Voting")
    for agent, (name, opinion, _) in zip(agents, agent_opinions):
        approve = opinion == "Approve"
        tx = contract.functions.vote(proposal_id, name, approve).transact()
        receipt_vote = web3.eth.wait_for_transaction_receipt(tx)
        st.write(f"{name} voted {'\u2705 Approve' if approve else '\u274C Reject'} (TX: {receipt_vote.transactionHash.hex()})")

    tx_finalize = contract.functions.finalizeProposal(proposal_id).transact()
    receipt_finalize = web3.eth.wait_for_transaction_receipt(tx_finalize)
    st.success(f"\U0001F3C1 Final Decision: {decision}")
    st.caption(f"Finalization TX: {receipt_finalize.transactionHash.hex()}")

    st.balloons()
