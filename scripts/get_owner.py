import pathlib
from brownie import accounts, config
from web3 import Web3


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7546"))

contract_address = pathlib.Path("utils/address.txt").read_text()
abi = pathlib.Path("utils/abi.json").read_text()
# with open("./contract_data/abi.json") as file_b:
#    contract_abi = file_b.read()

# initialising the contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=abi)


def main():
    print(f"owner: {str(contract_instance.functions.getOwner().call())}")
