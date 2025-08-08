#!/usr/bin/env python3
"""
Demo script showing how to use the blockchain directly.
This script demonstrates the blockchain functionality without the web interface.
"""

from blockchain import Blockchain
import time

def demo_blockchain():
    """Demonstrate blockchain functionality"""
    print("🔗 Simple Blockchain Demo")
    print("=" * 40)
    
    # Create a new blockchain
    print("\n1. Creating a new blockchain...")
    blockchain = Blockchain()
    print(f"✅ Blockchain created with {len(blockchain.chain)} blocks (genesis block)")
    
    # Create some transactions
    print("\n2. Creating transactions...")
    transactions = [
        ("alice", "bob", 50),
        ("bob", "charlie", 30),
        ("alice", "david", 20),
        ("charlie", "eve", 15)
    ]
    
    for sender, recipient, amount in transactions:
        index = blockchain.add_transaction(sender, recipient, amount)
        print(f"✅ Transaction: {sender} → {recipient} ({amount}) - Will be in block {index}")
    
    # Show pending transactions
    print(f"\n3. Pending transactions: {len(blockchain.pending_transactions)}")
    for tx in blockchain.pending_transactions:
        print(f"   {tx['from']} → {tx['to']} ({tx['amount']})")
    
    # Mine a block
    print("\n4. Mining a new block...")
    start_time = time.time()
    new_block = blockchain.mine_pending_transactions("miner1")
    end_time = time.time()
    
    print(f"✅ Block mined successfully!")
    print(f"   Block index: {new_block.index}")
    print(f"   Block hash: {new_block.hash}")
    print(f"   Nonce: {new_block.nonce}")
    print(f"   Mining time: {end_time - start_time:.2f} seconds")
    print(f"   Transactions in block: {len(new_block.transactions)}")
    
    # Create more transactions
    print("\n5. Creating more transactions...")
    more_transactions = [
        ("david", "frank", 10),
        ("eve", "alice", 25),
        ("frank", "bob", 5)
    ]
    
    for sender, recipient, amount in more_transactions:
        index = blockchain.add_transaction(sender, recipient, amount)
        print(f"✅ Transaction: {sender} → {recipient} ({amount}) - Will be in block {index}")
    
    # Mine another block
    print("\n6. Mining another block...")
    start_time = time.time()
    new_block2 = blockchain.mine_pending_transactions("miner2")
    end_time = time.time()
    
    print(f"✅ Block mined successfully!")
    print(f"   Block index: {new_block2.index}")
    print(f"   Block hash: {new_block2.hash}")
    print(f"   Nonce: {new_block2.nonce}")
    print(f"   Mining time: {end_time - start_time:.2f} seconds")
    
    # Show blockchain status
    print(f"\n7. Blockchain status:")
    print(f"   Total blocks: {len(blockchain.chain)}")
    print(f"   Chain valid: {blockchain.is_chain_valid()}")
    print(f"   Pending transactions: {len(blockchain.pending_transactions)}")
    
    # Show balances
    print(f"\n8. Balances:")
    addresses = ["alice", "bob", "charlie", "david", "eve", "frank", "miner1", "miner2"]
    for address in addresses:
        balance = blockchain.get_balance(address)
        print(f"   {address}: {balance}")
    
    # Show blockchain structure
    print(f"\n9. Blockchain structure:")
    for i, block in enumerate(blockchain.chain):
        print(f"   Block {i}:")
        print(f"     Hash: {block.hash[:20]}...")
        print(f"     Previous: {block.previous_hash[:20]}...")
        print(f"     Nonce: {block.nonce}")
        print(f"     Transactions: {len(block.transactions)}")
        if block.transactions:
            for tx in block.transactions:
                print(f"       {tx['from']} → {tx['to']} ({tx['amount']})")
        print()
    
    print("=" * 40)
    print("🎉 Demo completed!")
    print("\n💡 Key features demonstrated:")
    print("   - Transaction creation and management")
    print("   - Proof-of-work mining")
    print("   - Block linking and validation")
    print("   - Balance tracking")
    print("   - Chain integrity verification")

if __name__ == "__main__":
    demo_blockchain() 