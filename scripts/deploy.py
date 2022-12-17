import json
from brownie import Lottery, accounts

def main():
    # Compile and deploy the contract
    admin = accounts[0]
    myContract = Lottery.deploy({"from": admin})

    # Get the contract address
    contract_address = myContract.address
    print(contract_address)
    print("admin of the lottery: ", admin)
    #print(myContract.getIdentificationNumber())
    #print(myContract.participantsInfo())
    
    with open("utils/address.txt", "w") as file:
        file.write(contract_address)
    abi = myContract.abi
    json_object = json.dumps(abi)
    
    with open("utils/abi.json", "w") as file:
        file.write(json_object)