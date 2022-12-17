from flask import Flask, render_template, request, jsonify
from web3 import Web3
import json
from hexbytes import HexBytes
import os
import logging
import asyncio
from solcx import compile_source
import ast
app = Flask(__name__)
app.config['DEBUG'] = True
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
# compiled_sol = compile_source(
#      '''// SPDX-License-Identifier: MIT
# // Final project for Distributed Systems course, Universita della Svizzera italiana
# // Team members - Timur Taepov, De Grandi Alessandro, Filippo Casari

# pragma solidity ^0.8.17;

# contract Lottery{
#     // Let's define variables

#     address public boss; // This is person/owner of the lottery

#     uint public identificationNumber; // This is an ID number of the lottery

#     uint public identificationNumberMax = 100; // We set this amount to 100 -> this is
#                                                // a limit
 
#     uint public minPlayersNum = 1; // Set a minimal amount of players to search for
#                                    // a winner

#     address payable[] public participants; // This is an array where participants ETH
#     // addresses will be stored

#     address[] public winners; // This is an array of winners. It's not payable obviously

#     // Let's create a constructor which runs if our contract is deployed
#     // Runs only once when the contract is deployed
#     constructor(){

#         boss = msg.sender;
#         //participants.push(payable(boss));
#         identificationNumber = 0; // Initialize the ID number of the lottery to zero

#     }
#     function getOwner(
#     ) public view returns (address) {    
#         return boss;
#     }


#     // Write a function which really allows a user to join the lottery
#     // the function is payable because you can literally pass a certain amount of ETH
#     // and that amount will be stored inside of the contract address. Money are going
#     // inside to a contract pool
#     function joinLottery() public payable{ 

#         require(msg.value >= 0.015 ether); // Here we set the minimal amount of money
#         // which let the user to participate,
#         // thus it is 0.015 ETH

#         // If the number of ID is more than 100, the lottery can't be joined
#         //require(remainingIdentificationNumbers() <= identificationNumberMax, "You can't join the lottery");
#         address payable sender =payable (msg.sender);
#         participants.push(sender);
#         //participants.push(payable(sender)); // Push the address of whoever logged
        
#         // with a metamask to a players array

#     }

#     // Write a function which shows us a balance of the pool
#     function balanceCheck() public view returns(uint){

#         // We use "this" because we refer to a certain contract, the one we wrote
#         // Don't forget that this returns amount of WEI

#         return address(this).balance;

#     }

#     function getIdentificationNumber() public view returns(uint){

#         // Just return ID of the lottery
#         return identificationNumber;

#     }

#     function remainingIdentificationNumbers() public view returns (uint) {

#         // This function returns the remaining amount of ID which are available
#         // for lottery
#         return identificationNumberMax - getIdentificationNumber();

#     }

#     // Here we will grab the total amount of users, so that we can see the wallet
#     // addresses
#     function participantsInfo() public view returns (address payable[] memory){

#         // Yes, that is so easy, just return an array of participants
#         return participants;

#     }

#     // Write a function which will randomly pick a winner
#     function returnRandom() public view returns(uint){

#         // This contract employs Keccak as a hashing function. In most context
#         // specifically Keccak-256 is used, providing 32-byte hashes.
#         // Keccak is the leading hashing function, designed by non-NSA designers.
#         return uint(keccak256(abi.encodePacked(boss, block.timestamp)));

#     }

#     // Write a function which can pick a winner
#     // Only the contract owner is allowed to call this function
#     function selectWinner() public{

#         require(msg.sender == boss); // Only "boss" required to randomly pick a winner

#         // Check if we have three or more players
#         require(participants.length >=  minPlayersNum, "Not enough players");

#         uint randomNum = returnRandom() % participants.length; // This function
#         // selects a winner by index of the participants. For example we have three
#         // players: [first, second, third], the function takes random number selects
#         // a winner. This can do a modular divison and the residuals will always be
#         // in the range which is equal to the length of a participants

#         participants[randomNum].transfer(address(this).balance); // Take the funds
#         // from our contract address/pool and transfer money to a winner

#         winners.push(participants[randomNum]); // Grab the winners and push the
#         // player that was the winner. In another words we push an index of the
#         // person who win

#         identificationNumber++; // Since the lottery is done we can increment the
#         // lottery ID, obviously because lottery is over

#         //participants = new address payable[](0); // Clear an array of participants

#     }


#     // Let's show a winner
#     function showWinner() public view returns (address[] memory){

#         // Just return an array of addresses
#         return winners;

#     }

# }
#      ''',
#      output_values=['abi', 'bin']
#      )

# contract_id, contract_interface = compiled_sol.popitem()
# bytecode = contract_interface['bin']
# abi = contract_interface['abi']
# web3.eth.default_account = web3.eth.accounts[0]
# Greeter = web3.eth.contract(abi=abi, bytecode=bytecode)
# tx_hash = Greeter.constructor().transact()
# tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
# contract_instance = web3.eth.contract(
#     address=tx_receipt.contractAddress,
#      abi=abi
#  )
# print(contract_instance.functions.getOwner().call())

class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)





with open("../utils/address.txt") as file_a:
    contract_address = file_a.read()
with open("../utils/abi.json") as file_a:
    abi = file_a.read()
    abi = json.loads(abi)
# with open("./contract_data/abi.json") as file_b:
#    contract_abi = file_b.read()

# initialising the contract instance
bytecode = web3.eth.get_code(contract_address)
# if bytecode == '0x':
#     print("Contract has not been deployed")
# else:
#     print("Contract bytecode:", bytecode)
contract_instance = web3.eth.contract(address=contract_address, abi=abi)

@app.route('/')
def index():
    remainingIdNumbers = contract_instance.functions.remainingIdentificationNumbers().call()
    return render_template('index.html', remaining_id_numbers=remainingIdNumbers,owner= contract_instance.functions.getOwner().call(), id_number=contract_instance.functions.getIdentificationNumber().call())


@app.route('/get_owner', methods=['GET'])
def get_owner():

    owner = (contract_instance.functions.getOwner().call())
    return str(owner)


@app.route('/get_balance', methods=['GET'])
def get_balance():

    # Call the balanceCheck() function and retrieve the return value
    balance = contract_instance.functions.balanceCheck().call()

    # Check the return value of the balanceCheck() function
    if isinstance(balance, str) and balance.startswith("0x"):
        # The return value is a hexadecimal string, so it is in the correct format
        return balance
    else:
        # The return value is not a hexadecimal string, so it is not in the correct format
        return "Error: The balanceCheck() function returned an invalid value"


@app.route('/join_lottery', methods=['POST'])
def join_lottery():
    adress = request.form['adress']
    value = request.form['value']
    # me = web3.eth.accounts[1]
    sender = Web3.toChecksumAddress(adress)
    value = web3.toWei(int(value), "ether")
    txn = {
        "from": sender,
        "value": value,
    }
    try:
        txn_hash = contract_instance.functions.joinLottery().transact(txn)
        tx_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
        result = contract_instance.functions.participantsInfo().call()
        print(result)
        
        tx_dict = dict(tx_receipt)

        
        return render_template("joinLottery.html", account=tx_dict["from"])
    except Exception as error:
        return str(error)

@app.route('/participantsInfo', methods=['GET'])
def get_participants_info():
    try:
        # Call the contract's participantsInfo() function
    
        result = contract_instance.functions.participantsInfo().call()
        #print(contract_instance.functions)
        print(type(result))
        
        
        # Return the result as a JSON object
        return render_template('participants.html', items=result)
    except Exception as error:
        return str(error)

@app.route('/balanceCheck', methods=['GET'])
def balanceCheck():
    try:
        # Call the contract's participantsInfo() function
    
        result = contract_instance.functions.balanceCheck().call()
        #print(contract_instance.functions)
        print(result)
        # Return the result as a JSON object
        return render_template('safe.html', balance=result)
    except Exception as error:
        return str(error)

@app.route('/selectWinner', methods=['POST'])
def select_winner():
    address = request.form['adress']
    print(address)
    sender = Web3.toChecksumAddress(address)
    txn = {
        "from": sender,
    }
    try:
        # Call the contract's selectWinner() function
        txn_hash = contract_instance.functions.selectWinner().transact(txn)
        tx_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
        winners = contract_instance.functions.showWinner().call()
        
        return render_template("winner.html", winner=winners[-1], history=winners)
        # Return the transaction receipt as a JSON object
        
    except Exception as error:
        return str(error)
    
@app.route('/getIdentificationNumber', methods=['POST'])
def getIdentificationNumber():
    
    try:
        
        # Call the contract's selectWinner() function
        result=contract_instance.functions.getIdentificationNumber().call()
        return json.dumps(result, cls=HexJsonEncoder)
        # Return the transaction receipt as a JSON object
        
    except Exception as error:
        return str(error) 



if __name__ == '__main__':
    from waitress import serve
    serve(app, port=5000)
    #app.run(port=5000)
