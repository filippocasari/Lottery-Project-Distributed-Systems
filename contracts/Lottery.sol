// SPDX-License-Identifier: MIT
// Final project for Distributed Systems course, Universita della Svizzera italiana
// Team members - Timur Taepov, De Grandi Alessandro, Filippo Casari

pragma solidity ^0.8.17;

contract Lottery{
    // Let's define variables

    address public boss; // This is person/owner of the lottery

    uint public identificationNumber; // This is an ID number of the lottery

    uint public identificationNumberMax = 100; // We set this amount to 100 -> this is
                                               // a limit
 
    uint public minPlayersNum = 1; // Set a minimal amount of players to search for
                                   // a winner

    address payable[] public participants; // This is an array where participants ETH
    // addresses will be stored

    address[] public winners; // This is an array of winners. It's not payable obviously

    // Let's create a constructor which runs if our contract is deployed
    // Runs only once when the contract is deployed
    constructor(){

        boss = msg.sender;
        //participants.push(payable(boss));
        identificationNumber = 0; // Initialize the ID number of the lottery to zero

    }
    function getOwner(
    ) public view returns (address) {    
        return boss;
    }
    function isParticipant(address payable _address) public view returns (bool) {
    for (uint i = 0; i < participants.length; i++) {
        if (participants[i] == _address) {
            return true;
        }
    }
    return false;
}



    // Write a function which really allows a user to join the lottery
    // the function is payable because you can literally pass a certain amount of ETH
    // and that amount will be stored inside of the contract address. Money are going
    // inside to a contract pool
    function joinLottery() public payable{ 

        require(msg.value >= 0.015 ether); // Here we set the minimal amount of money
        // which let the user to participate,
        // thus it is 0.015 ETH

        // If the number of ID is more than 100, the lottery can't be joined
        require(remainingIdentificationNumbers() <= identificationNumberMax, "You can't join the lottery");
        address payable sender =payable (msg.sender);
        //require(isParticipant(sender) == false, "You already are a participant");
        participants.push(sender);
        //participants.push(payable(sender)); // Push the address of whoever logged
        
        // with a metamask to a players array

    }

    // Write a function which shows us a balance of the pool
    function balanceCheck() public view returns(uint){

        // We use "this" because we refer to a certain contract, the one we wrote
        // Don't forget that this returns amount of WEI

        return address(this).balance;

    }

    function getIdentificationNumber() public view returns(uint){

        // Just return ID of the lottery
        return identificationNumber;

    }

    function remainingIdentificationNumbers() public view returns (uint) {

        // This function returns the remaining amount of ID which are available
        // for lottery
        return identificationNumberMax - getIdentificationNumber();

    }

    // Here we will grab the total amount of users, so that we can see the wallet
    // addresses
    function participantsInfo() public view returns (address payable[] memory){

        // Yes, that is so easy, just return an array of participants
        return participants;

    }

    // Write a function which will randomly pick a winner
    function returnRandom() public view returns(uint){

        // This contract employs Keccak as a hashing function. In most context
        // specifically Keccak-256 is used, providing 32-byte hashes.
        // Keccak is the leading hashing function, designed by non-NSA designers.
        return uint(keccak256(abi.encodePacked(boss, block.timestamp)));

    }

    // Write a function which can pick a winner
    // Only the contract owner is allowed to call this function
    function selectWinner() public{

        require(msg.sender == boss, "your not the lottery boss"); // Only "boss" required to randomly pick a winner

        // Check if we have three or more players
        require(participants.length >=  minPlayersNum, "Not enough players");

        uint randomNum = returnRandom() % participants.length; // This function
        // selects a winner by index of the participants. For example we have three
        // players: [first, second, third], the function takes random number selects
        // a winner. This can do a modular divison and the residuals will always be
        // in the range which is equal to the length of a participants

        participants[randomNum].transfer(address(this).balance); // Take the funds
        // from our contract address/pool and transfer money to a winner

        winners.push(participants[randomNum]); // Grab the winners and push the
        // player that was the winner. In another words we push an index of the
        // person who win

        identificationNumber++; // Since the lottery is done we can increment the
        // lottery ID, obviously because lottery is over

        participants = new address payable[](0); // Clear an array of participants

    }


    // Let's show a winner
    function showWinner() public view returns (address[] memory){

        // Just return an array of addresses
        return winners;

    }

}