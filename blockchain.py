import hashlib
import json
import time
from typing import List, Dict, Any
from urllib.parse import urlparse
import requests


class Block:
    def __init__(self, index: int, transactions: List[Dict], timestamp: float, previous_hash: str):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculate the hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 4  # Number of leading zeros required
        self.pending_transactions: List[Dict] = []
        self.mining_reward = 10
        self.nodes = set()
        
        # Create the genesis block
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]

    def mine_pending_transactions(self, miner_address: str) -> Block:
        """Mine a new block with pending transactions"""
        # Create a new block with pending transactions
        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.get_latest_block().hash
        )

        # Mine the block
        self.proof_of_work(block)

        # Add the block to the chain
        self.chain.append(block)

        # Reset pending transactions and add mining reward
        self.pending_transactions = [
            {
                'from': 'network',
                'to': miner_address,
                'amount': self.mining_reward
            }
        ]

        return block

    def proof_of_work(self, block: Block):
        """Proof of work algorithm"""
        while block.hash[:self.difficulty] != '0' * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()

    def add_transaction(self, sender: str, recipient: str, amount: float) -> int:
        """Add a new transaction to pending transactions"""
        self.pending_transactions.append({
            'from': sender,
            'to': recipient,
            'amount': amount
        })
        return self.get_latest_block().index + 1

    def get_balance(self, address: str) -> float:
        """Get the balance of a given address"""
        balance = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction['from'] == address:
                    balance -= transaction['amount']
                if transaction['to'] == address:
                    balance += transaction['amount']

        return balance

    def is_chain_valid(self) -> bool:
        """Check if the blockchain is valid"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if the previous hash is correct
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def add_node(self, address: str):
        """Add a new node to the list of nodes"""
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self) -> bool:
        """Replace the current chain with the longest valid chain from other nodes"""
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            try:
                response = requests.get(f'http://{node}/chain')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    if length > max_length and self.is_chain_valid():
                        max_length = length
                        longest_chain = chain
            except:
                continue

        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert the blockchain to a dictionary for JSON serialization"""
        return {
            'chain': [
                {
                    'index': block.index,
                    'transactions': block.transactions,
                    'timestamp': block.timestamp,
                    'previous_hash': block.previous_hash,
                    'nonce': block.nonce,
                    'hash': block.hash
                }
                for block in self.chain
            ],
            'pending_transactions': self.pending_transactions,
            'length': len(self.chain)
        } 