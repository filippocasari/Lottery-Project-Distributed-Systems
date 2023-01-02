from flask import Flask, render_template, request
from web3 import Web3
import json
from hexbytes import HexBytes

# from solcx import compile_source if we wanna compile the contract directly here, instead of using brownie

app = Flask(__name__)
app.config['DEBUG'] = True
port = 7546 # can be set according with ganache
web3 = Web3(Web3.HTTPProvider(f'http://127.0.0.1:{port}')) 


class HexJsonEncoder(json.JSONEncoder):
    """custom parser

    Args:
        json (json.JSONEncoder):json.JSONEncoder
    """    
    def default(self, obj):
        return obj.hex() if isinstance(obj, HexBytes) else super().default(obj)


import pathlib
contract_address = pathlib.Path("../utils/address.txt").read_text()
with open("../utils/abi.json") as file_a:
    abi = file_a.read()
    abi = json.loads(abi)
    
bytecode = web3.eth.get_code(contract_address)
# if bytecode == '0x':
#     print("Contract has not been deployed")
# else:
#     print("Contract bytecode:", bytecode)
contract_instance = web3.eth.contract(address=contract_address, abi=abi)


@app.route('/')
def index():
    """
    This is the main page
    Returns:
        str: Render a template by name with the given context
    """    
    remainingIdNumbers = contract_instance.functions.remainingIdentificationNumbers().call()
    return render_template('index.html', remaining_id_numbers=remainingIdNumbers, owner=contract_instance.functions.getOwner().call(), id_number=contract_instance.functions.getIdentificationNumber().call())


@app.route('/get_owner', methods=['GET'])
def get_owner():
    """get the name of the owner, NOT implemented, not necessary

    Returns:
        str: name of the owner
    """    
    owner = (contract_instance.functions.getOwner().call())
    return str(owner)


@app.route('/get_balance', methods=['GET'])
def get_balance():
    """get the balance of the contract

    Returns:
        str: balance of solidity contract
    """    
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
    """an account can join the lottery

    Returns:
        str: see the html
    """    
    adress = request.form['adress']
    # request.form['value']
    #value_in_wei = int(0.016 * 10**18)
    # me = web3.eth.accounts[1]
    sender = Web3.toChecksumAddress(adress)

    value = web3.toWei(0.015, "ether")

    print(value)
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
    """returns the list of participants

    Returns:
        str: list of participants, or empty list if no participants
    """    
    try:
        # Call the contract's participantsInfo() function

        result = contract_instance.functions.participantsInfo().call()
        # print(contract_instance.functions)
        print(type(result))

        # Return the result as a JSON object
        return render_template('participants.html', items=result)
    except Exception as error:
        return str(error)


@app.route('/balanceCheck', methods=['GET'])
def balanceCheck():
    """show the balance of the contract

    Returns:
       str: balance
    """    
    try:
        # Call the contract's participantsInfo() function

        result = contract_instance.functions.balanceCheck().call()
        # print(contract_instance.functions)
        print(result)
        # Return the result as a JSON object
        return render_template('safe.html', balance=result)
    except Exception as error:
        return str(error)


@app.route('/selectWinner', methods=['POST'])
def select_winner():
    """select and show the winner

    Returns:
        str: winner and the list of previous winners
    """    
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
    """get the identifier number of the lottery

    Returns:
        str: positive number of the lottery
    """    
    try:

        # Call the contract's selectWinner() function
        result = contract_instance.functions.getIdentificationNumber().call()
        return json.dumps(result, cls=HexJsonEncoder)
        # Return the transaction receipt as a JSON object

    except Exception as error:
        return str(error)


if __name__ == '__main__':
    from waitress import serve
    serve(app, port=5000)
    # app.run(port=5000)
