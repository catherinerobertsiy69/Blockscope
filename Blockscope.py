import json
import time
from web3 import Web3
import requests

INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # Замените на свой ключ
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def is_contract(address):
    code = w3.eth.get_code(address)
    return code != b''

def get_recent_blocks(n=10):
    latest = w3.eth.block_number
    return [w3.eth.get_block(i, full_transactions=True) for i in range(latest - n + 1, latest + 1)]

def analyze_blocks():
    print("🔍 Starting Blockscope scan...")
    touched_contracts = {}
    for block in get_recent_blocks():
        for tx in block.transactions:
            to = tx.to
            if to and w3.is_address(to) and is_contract(to):
                if to not in touched_contracts:
                    code_size = len(w3.eth.get_code(to))
                    balance = w3.eth.get_balance(to)
                    if balance == 0:
                        print(f"⚠️ Contract {to} was just touched but has zero balance. Might be awakening!")
                        touched_contracts[to] = {
                            "block": block.number,
                            "tx": tx.hash.hex(),
                            "from": tx['from']
                        }
    print("✅ Scan complete.")

if __name__ == "__main__":
    while True:
        analyze_blocks()
        print("⏱️ Waiting 60 seconds...")
        time.sleep(60)
