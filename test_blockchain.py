#!/usr/bin/env python3
"""
Test script for the blockchain implementation.
This script demonstrates the core functionality of the blockchain.
"""

import requests
import json
import time

# Base URL for the blockchain API
BASE_URL = "http://localhost:5001"

def test_blockchain():
    """Test the blockchain functionality"""
    print("🚀 Testing Simple Blockchain Implementation")
    print("=" * 50)
    
    # Test 1: Get the initial chain
    print("\n1. Getting initial blockchain...")
    try:
        response = requests.get(f"{BASE_URL}/chain")
        if response.status_code == 200:
            chain_data = response.json()
            print(f"✅ Initial chain length: {chain_data['length']}")
            print(f"   Genesis block hash: {chain_data['chain'][0]['hash'][:20]}...")
        else:
            print("❌ Failed to get initial chain")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to blockchain server. Make sure the server is running on http://localhost:5001")
        return
    
    # Test 2: Create some transactions
    print("\n2. Creating transactions...")
    transactions = [
        {"sender": "alice", "recipient": "bob", "amount": 50},
        {"sender": "bob", "recipient": "charlie", "amount": 30},
        {"sender": "alice", "recipient": "david", "amount": 20}
    ]
    
    for i, transaction in enumerate(transactions, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/transactions/new",
                json=transaction,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 201:
                print(f"✅ Transaction {i}: {transaction['sender']} → {transaction['recipient']} ({transaction['amount']})")
            else:
                print(f"❌ Failed to create transaction {i}")
        except Exception as e:
            print(f"❌ Error creating transaction {i}: {e}")
    
    # Test 3: Check pending transactions
    print("\n3. Checking pending transactions...")
    try:
        response = requests.get(f"{BASE_URL}/pending")
        if response.status_code == 200:
            pending = response.json()['pending_transactions']
            print(f"✅ Pending transactions: {len(pending)}")
            for tx in pending:
                print(f"   {tx['from']} → {tx['to']} ({tx['amount']})")
        else:
            print("❌ Failed to get pending transactions")
    except Exception as e:
        print(f"❌ Error getting pending transactions: {e}")
    
    # Test 4: Mine a block
    print("\n4. Mining a new block...")
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/mine")
        end_time = time.time()
        
        if response.status_code == 200:
            block_data = response.json()
            print(f"✅ Block mined successfully!")
            print(f"   Block index: {block_data['index']}")
            print(f"   Block hash: {block_data['hash'][:20]}...")
            print(f"   Nonce: {block_data['nonce']}")
            print(f"   Mining time: {end_time - start_time:.2f} seconds")
            print(f"   Transactions in block: {len(block_data['transactions'])}")
        else:
            print("❌ Failed to mine block")
    except Exception as e:
        print(f"❌ Error mining block: {e}")
    
    # Test 5: Check chain validity
    print("\n5. Checking chain validity...")
    try:
        response = requests.get(f"{BASE_URL}/valid")
        if response.status_code == 200:
            validity = response.json()['is_valid']
            if validity:
                print("✅ Blockchain is valid")
            else:
                print("❌ Blockchain is invalid")
        else:
            print("❌ Failed to check validity")
    except Exception as e:
        print(f"❌ Error checking validity: {e}")
    
    # Test 6: Get updated chain
    print("\n6. Getting updated blockchain...")
    try:
        response = requests.get(f"{BASE_URL}/chain")
        if response.status_code == 200:
            chain_data = response.json()
            print(f"✅ Updated chain length: {chain_data['length']}")
            print(f"   Latest block hash: {chain_data['chain'][-1]['hash'][:20]}...")
        else:
            print("❌ Failed to get updated chain")
    except Exception as e:
        print(f"❌ Error getting updated chain: {e}")
    
    # Test 7: Check balances
    print("\n7. Checking balances...")
    addresses = ["alice", "bob", "charlie", "david"]
    for address in addresses:
        try:
            response = requests.get(f"{BASE_URL}/balance/{address}")
            if response.status_code == 200:
                balance = response.json()['balance']
                print(f"✅ {address}: {balance}")
            else:
                print(f"❌ Failed to get balance for {address}")
        except Exception as e:
            print(f"❌ Error getting balance for {address}: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Blockchain testing completed!")
    print("\n💡 Tips:")
    print("   - Visit http://localhost:5001 to see the web interface")
    print("   - Try creating more transactions and mining blocks")
    print("   - Experiment with different addresses and amounts")

if __name__ == "__main__":
    test_blockchain() 