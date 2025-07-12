# 🧠 Agentic Patent Review Council

A proof-of-concept system that simulates a council of autonomous AI agents reviewing patent submissions. The agents debate the novelty of submitted ideas, vote on their patent-worthiness, and record the final decision on a blockchain smart contract. Everything is wrapped with an easy-to-use `Streamlit` interface.

---

## 📌 Features

- ✅ Submit patent proposals via a **Streamlit Web UI**
- 🤖 Specialized AI agents (novelty checker, debater, voter)
- 🔍 Searches Google Patents for prior art
- 🗳️ Decentralized consensus voting among agents
- ⛓️ Results recorded immutably on an Ethereum test blockchain (via Ganache)
- 📈 Real-time final decision display on the frontend

---

## 📁 Project Structure

```
AI_Patent_Review_Council/
│
├── ai_novelty_agent.py         # Agent to check novelty of a proposal
├── multiagent.py               # Agent debate and voting orchestration
├── streamlit_app.py            # Streamlit UI for proposal submission and final decision
│
├── patent_search.py            # Searches for similar patents via Google Patents
│
├── dao_contract.sol            # Solidity smart contract (DAOCouncil)
├── dao_contract_abi.json       # ABI JSON for contract interaction
├── dao_contract_bytecode.txt   # Compiled contract bytecode
├── compile_dao.py              # Python script to compile Solidity contract
├── deploy_contract.py          # Python script to deploy contract to Ganache
│
├── example.txt                 # Sample patent proposal format
├── flow_diagram.txt            # Textual flow diagram of the system
├── __pycache__/                # Python cache (ignored in production)
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+
- [Ganache](https://trufflesuite.com/ganache/) (for local blockchain)
- MetaMask (optional, for blockchain inspection)
- Node.js + `solc` compiler (optional)

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/gaurav1kr/Hackathons.git
cd Hackathons/AI_Patent_Review_Council
```

---

### 2️⃣ Install Python Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> If `requirements.txt` is missing, install at minimum:
```bash
pip install streamlit openai web3 googlesearch-python
```

---

### 3️⃣ Start Ganache

Run Ganache on `http://127.0.0.1:7545` and ensure a default account is available.

---

### 4️⃣ Compile and Deploy the Smart Contract

```bash
python compile_dao.py
python deploy_contract.py
```

This will compile `dao_contract.sol` and deploy it to the local blockchain.

---

### 5️⃣ Launch the Streamlit UI

```bash
streamlit run streamlit_app.py
```

---

## 🧠 How It Works

1. Users submit a **title** and **description** for a patent idea.
2. The **AI Novelty Agent** performs keyword extraction and searches Google Patents.
3. Multiple **AI agents debate** and vote internally on the novelty.
4. The final vote is **committed to the blockchain** via a smart contract.
5. The user sees the **decision and explanation** in the UI.

---

## ⛓️ Smart Contract Overview

- `dao_contract.sol`: Defines `submitProposal`, `vote`, `getDecision`.
- Votes and final status are stored on-chain in Ganache.
- Interacted via `web3.py` from Python backend.

---

## 📊 Flow Diagram

You can find a textual system flow in `flow_diagram.txt`.

```
[User] --> [Streamlit UI] --> [Submit Proposal]
[Streamlit UI] --> [AI Agents Debate]
[AI Agents] --> [Votes to Blockchain]
[Blockchain] --> [Final Decision Display]
```

---

## 💡 Example Proposal Format

See `example.txt`:

```
Title: Smart Helmet for Motorcycle Safety
Description: A helmet equipped with impact sensors...
```

---

## 🛠️ Future Improvements

- Real-time GPT-based dialogue between agents
- Enhanced explainability in decisions
- Integration with public blockchain (Polygon testnet)
- OAuth for authenticated submissions
- Multi-modal inputs (PDF diagrams, claims, etc.)

---

## 📜 License

MIT License — use freely with attribution.

---

## 🙌 Credits

- **Gaurav Sinha** — Creator and Architect
- **OpenAI** — AI agent generation and patent analysis logic
- **Ethereum + Ganache** — Decentralized decision recording

---

## 📬 Contact

Feel free to raise an issue or ping at [your-email@example.com].

---

*Bringing fairness and intelligence to innovation, one agent at a time.*
