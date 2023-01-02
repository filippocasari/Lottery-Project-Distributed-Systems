from brownie import Lottery, accounts
import pytest

# Deploy the contract, and return it. It will be called whenever a test needs it
@pytest.fixture
def lottery():
    return accounts[0].deploy(Lottery)
# Test the getOwner function
def test_get_owner(lottery):
    assert lottery.getOwner() == accounts[0]


def test_balance_account(lottery):
    #print("balance of account 0: ", accounts[1].balance())
    assert accounts[1].balance()> 0
    
# Test the joinLottery function
def test_join_lottery(lottery):
    lottery.joinLottery({"from": accounts[4], "value": 0.015*(10**18)})
    assert lottery.isParticipant(accounts[4]) == True

# Test the balanceCheck function
def test_balance_check(lottery):
    assert lottery.balanceCheck() == 0.015


# Test the getIdentificationNumber function
def test_get_identification_number(lottery):
    assert lottery.getIdentificationNumber() == 0

# Test the remainingIdentificationNumbers function
def test_remaining_identification_numbers(lottery):
    assert lottery.remainingIdentificationNumbers() == 100

def test_random(lottery):
    random_number = lottery.returnRandom()
    assert isinstance(random_number, int)


# Define a test function
def test_toy_example_lottery(lottery):
    # Test the getOwner function
    assert lottery.getOwner() == accounts[0]
    
    # Test the joinLottery function
    lottery.joinLottery({"from": accounts[1], "value": 0.015*(10**18)})
    assert lottery.isParticipant(accounts[1]) == True
    
    # Test the balanceCheck function
    balance = lottery.balanceCheck()
    assert balance ==  0.015*(10**18)
    
    # Test the getIdentificationNumber function
    assert lottery.getIdentificationNumber() == 0
    
    # Test the remainingIdentificationNumbers function
    assert lottery.remainingIdentificationNumbers() == 100
    
    # Test the participantsInfo function
    assert lottery.participantsInfo() == [accounts[1]]
    
    # Test the returnRandom function
    random_number = lottery.returnRandom()
    assert isinstance(random_number, int)
    
    # Test the selectWinner function
    lottery.selectWinner({"from": accounts[0]})
    assert lottery.showWinner() == [accounts[1]]

