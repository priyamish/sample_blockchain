# Simple Blockchain Implementation

A complete blockchain implementation using Python and Flask with a modern web interface.

## Features

- **Blockchain Core**: Complete blockchain implementation with blocks, transactions, and proof-of-work mining
- **Web API**: RESTful API endpoints for all blockchain operations
- **Web Interface**: Modern, responsive web UI built with Bootstrap
- **Transaction System**: Create and manage transactions between addresses
- **Mining**: Proof-of-work mining with configurable difficulty
- **Chain Validation**: Built-in validation to ensure blockchain integrity
- **Node Management**: Support for multiple nodes in a network

## Project Structure

```
sample_blockchain/
├── blockchain.py          # Core blockchain implementation
├── app.py                # Flask web application
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Web interface template
└── README.md            # This file
```

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd sample_blockchain
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:5001
   ```

## Usage

### Web Interface

The web interface provides an intuitive way to interact with the blockchain:

- **View Blockchain**: See all blocks, transactions, and chain statistics
- **Mine Blocks**: Click the "Mine Block" button to create new blocks
- **Create Transactions**: Use the form to send transactions between addresses
- **Monitor Status**: Real-time updates on chain validity and statistics

### API Endpoints

The blockchain also provides a REST API for programmatic access:

#### 1. Mine a Block
```http
GET /mine
```
Mines a new block with pending transactions.

#### 2. Create Transaction
```http
POST /transactions/new
Content-Type: application/json

{
    "sender": "alice",
    "recipient": "bob",
    "amount": 50
}
```

#### 3. Get Full Chain
```http
GET /chain
```
Returns the complete blockchain.

#### 4. Get Pending Transactions
```http
GET /pending
```
Returns all pending transactions.

#### 5. Check Chain Validity
```http
GET /valid
```
Returns whether the blockchain is valid.

#### 6. Get Balance
```http
GET /balance/<address>
```
Returns the balance of a specific address.

#### 7. Register Nodes
```http
POST /nodes/register
Content-Type: application/json

{
    "nodes": ["http://localhost:5001", "http://localhost:5002"]
}
```

#### 8. Resolve Conflicts
```http
GET /nodes/resolve
```
Resolves conflicts between nodes by accepting the longest valid chain.

## Example Usage with curl

### Mine a block:
```bash
curl -X GET http://localhost:5001/mine
```

### Create a transaction:
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "sender": "alice",
    "recipient": "bob", 
    "amount": 50
}' http://localhost:5001/transactions/new
```

### Get the full chain:
```bash
curl -X GET http://localhost:5001/chain
```

### Check chain validity:
```bash
curl -X GET http://localhost:5001/valid
```

## Blockchain Features

### Block Structure
Each block contains:
- **Index**: Position in the blockchain
- **Timestamp**: When the block was created
- **Transactions**: List of transactions in the block
- **Previous Hash**: Hash of the previous block
- **Nonce**: Number used in proof-of-work
- **Hash**: SHA256 hash of the block

### Proof of Work
The blockchain uses a proof-of-work algorithm where miners must find a nonce that produces a hash with a specified number of leading zeros (default: 4).

### Transaction System
- Transactions are added to a pending pool
- Mining a block includes all pending transactions
- Mining rewards are automatically added to the miner's address
- Balance calculation considers all transactions in the chain

### Security Features
- **Hash Linking**: Each block is linked to the previous block via hash
- **Chain Validation**: Built-in validation ensures chain integrity
- **Immutable History**: Once mined, blocks cannot be modified without breaking the chain

## Configuration

You can modify the blockchain parameters in `blockchain.py`:

- **Difficulty**: Change `self.difficulty` to adjust mining difficulty
- **Mining Reward**: Modify `self.mining_reward` to change the reward amount
- **Port**: Change the port in `app.py` if needed

## Multi-Node Setup

To run multiple nodes:

1. Start the first node on port 5001:
   ```bash
   python app.py
   ```

2. Start additional nodes on different ports by modifying the port in `app.py`:
   ```python
   app.run(host='0.0.0.0', port=5002, debug=True)
   ```

3. Register nodes with each other using the `/nodes/register` endpoint.

## Technical Details

### Dependencies
- **Flask**: Web framework for the API and web interface
- **requests**: HTTP library for node communication
- **hashlib**: For SHA256 hashing
- **json**: For data serialization
- **time**: For timestamps
- **uuid**: For generating unique node identifiers

### Algorithm
- **Hashing**: SHA256 for block hashing
- **Proof of Work**: Brute force nonce finding
- **Consensus**: Longest valid chain rule

## Contributing

Feel free to extend this blockchain implementation with additional features like:
- Wallet functionality with public/private key pairs
- Smart contracts
- Merkle trees for transaction verification
- Different consensus mechanisms
- Database persistence
- WebSocket support for real-time updates

## License

This project is open source and available under the MIT License.
