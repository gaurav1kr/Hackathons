from solcx import compile_source, install_solc
import json

# Install the required Solidity version
install_solc("0.8.19")

# Read the Solidity file
with open("dao_contract.sol", "r") as file:
    source_code = file.read()

# Compile
compiled = compile_source(source_code, output_values=["abi", "bin"], solc_version="0.8.19")
contract_id, contract_interface = compiled.popitem()

# Save ABI
with open("dao_contract_abi.json", "w") as f:
    json.dump(contract_interface["abi"], f)

# Save Bytecode
with open("dao_contract_bytecode.txt", "w") as f:
    f.write(contract_interface["bin"])
