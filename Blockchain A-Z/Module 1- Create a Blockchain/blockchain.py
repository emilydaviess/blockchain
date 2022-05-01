# module 1 -create a blockchain

# to be installed: 
    # Flask==0.12.2 pip install Flask==0.12.2
    # Postman HTTP Client: https:www.getpostman.com
    

# import the libraries 
import datetime
import hashlib
import json
from flask import Flask, jsonify

# part 1: building a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        # append block to chain
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        # get last block in the chain
        last_block = self.chain[-1]
        return(last_block)
    
    # this will be used to mine blocks
    def proof_of_work(self, previous_proof):
        new_proof = 1  # this is the Nonce
        check_proof = False
        while check_proof is False: 
            # the sha256 args cannot be symetrical (i.e. new_proof+previous_proof)
            # we've used **2 but the operation can really be anything, the harder the operation the better
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000': # check that the hash starts with four leading 0's
                check_proof = True
            else: 
                new_proof += 1 
        return(new_proof)
                
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
                
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        
        # validate all blocks in a chain, block by block
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
            

# part 2 - mining our blockchain

# create a web app using Flask
app = Flask(__name__)
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# create a blockchain
blockchain = Blockchain()

# mining a new block
@app.route('/mine_block', methods=['GET']) # Running on http://127.0.0.1:5000/
def mine_block():
    # first thing you need to do to mine a block, is to solve the proof problem
    # to solve the proof problem, you need to previous proof (from the previous block)
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message': "Congrats, you just mined a block!", 
                'index': block['index'], 
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
   
    return jsonify(response), 200 # 200 success code


# getting the full Blockchain
@app.route('/get_chain', methods=['GET']) # Running on http://127.0.0.1:5000/
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200 # 200 success code
 
# checking if the Blockchain is valid   
@app.route('/is_valid', methods=['GET']) # Running on http://127.0.0.1:5000/
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The blockchain is valid.'}
    else: 
        response = {'message': 'Houston, we had a problem.'}
    
    return jsonify(response), 200 # 200 success code
  
    

# running the app
app.run(host='0.0.0.0', port=5000) # host,port

# now run the whole file
# go to POSTMAN and c/p http://127.0.0.1:5000/get_chain to see the blockchain
# or go to http://127.0.0.1:5000/mine_block to mine another block into the chain
# you can re-visit http://127.0.0.1:5000/get_chain to monitor blocks being added to the chain