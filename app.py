from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain
import uuid

app = Flask(__name__)

# Create a unique identifier for this node
node_identifier = str(uuid.uuid4()).replace('-', '')

# Create the blockchain instance
blockchain = Blockchain()


@app.route('/')
def index():
    """Main page with blockchain information"""
    return render_template('index.html', 
                         chain=blockchain.chain,
                         pending_transactions=blockchain.pending_transactions,
                         node_identifier=node_identifier)


@app.route('/mine', methods=['GET'])
def mine():
    """Mine a new block"""
    # We run the proof of work algorithm to get the next proof
    last_block = blockchain.get_latest_block()
    previous_hash = last_block.hash

    # Create a new block with pending transactions
    block = blockchain.mine_pending_transactions(node_identifier)

    response = {
        'message': 'New block mined!',
        'index': block.index,
        'transactions': block.transactions,
        'previous_hash': block.previous_hash,
        'hash': block.hash,
        'nonce': block.nonce
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """Create a new transaction"""
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new transaction
    index = blockchain.add_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    """Get the full blockchain"""
    response = blockchain.to_dict()
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """Register a list of new nodes"""
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.add_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """Resolve conflicts between blockchain nodes"""
    replaced = blockchain.replace_chain()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.to_dict()
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.to_dict()
        }

    return jsonify(response), 200


@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """Get the balance of a specific address"""
    balance = blockchain.get_balance(address)
    response = {
        'address': address,
        'balance': balance
    }
    return jsonify(response), 200


@app.route('/pending', methods=['GET'])
def get_pending_transactions():
    """Get all pending transactions"""
    response = {
        'pending_transactions': blockchain.pending_transactions
    }
    return jsonify(response), 200


@app.route('/valid', methods=['GET'])
def is_valid():
    """Check if the blockchain is valid"""
    is_valid_chain = blockchain.is_chain_valid()
    response = {
        'is_valid': is_valid_chain
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 