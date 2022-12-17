from brownie import accounts, config
from web3 import Web3
# from eth_utils import from_wei


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

with open("utils/address.txt") as file_a:
    contract_address = file_a.read()
with open("utils/abi.json") as file_a:
    abi = file_a.read()
#with open("./contract_data/abi.json") as file_b:
#    contract_abi = file_b.read()

# initialising the contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=abi)


def main():
    print("owner: " + str(contract_instance.functions.getOwner()))
    

    