# deploy_contract.py

import json
from web3 import Web3
from web3.exceptions import ContractLogicError

# 1. === CONNECT TO GANACHE ===
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    raise ConnectionError("❌ Unable to connect to Ganache at http://127.0.0.1:7545")

# 2. === ABI and BYTECODE ===
with open("dao_contract_abi.json") as f:
    abi = json.load(f)

with open("dao_contract_bytecode.txt") as f:
    bytecode = f.read().strip()

# 3. === SET ACCOUNT ===
web3.eth.default_account = web3.eth.accounts[0]

# 4. === DEPLOY CONTRACT ===
try:
    print("🚀 Deploying contract...")
    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = receipt.contractAddress
    print(f"✅ Deployed at: {contract_address}")
except ContractLogicError as e:
    print(f"❌ Deployment failed: {str(e)}")
except Exception as e:
    print(f"⚠️ Unexpected error: {str(e)}")
