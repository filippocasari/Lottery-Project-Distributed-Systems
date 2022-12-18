# Lottery Project Distributed System
@authors: Filippo Casari, Alessandro De Grandi, Timur Taepov
## Structure & Commands
### Brownie
The project has been initialised by brownie. (*DO NOT* run this command)
```python
brownie init
```
We have several dirs. One of them is "contracts" in which there is our solidity contract. 
To compile the contract we run:
```python
brownie compile
```
It creates the dir "build".
We need now to add ganache network to work on. Run the following command to to that:
```python
brownie networks add Ethereum local host='http://127.0.0.1:7545' chainid=5776
```
Note: [port] and [chainid] depend on your ganache configuration. [local] is just a name for your network, you can modify it as you prefer. 
Now you have to deploy the contract. Just run :
```console
brownie run deploy.py --network local
```
deploy.py is a python script within the dir "scripts". If you get an error, probably you do not have a dir "utils" where deploy.py is trying to save the contract's specification used afterwords by app.py. To fix it, just create utils directory by running in the root dir:
```shell
mkdir utils
```
### WEb3 & Flask
Flask has been used for the backend of our server whereas Web3 is a Python library for interacting with Ethereum. Both needed to be installed by :
```shell
pip install web3 flask
```
To run the application flask you have to run in "src" dir:
```console
flask run
```
This will start the server @ip:port specified in "src/app.py". 

Now open chrome and paste in the navigation bar:
```console
http://127.0.0.1:5000
```
Note: the port can be set in app.py. 5000 is written by default in app.py script. 
Now you have to access to your matamask account. You should import your matamask accounts by inserting the private keys of your ganache blockchain. \
Guidelines: https://www-geeksforgeeks-org.translate.goog/how-to-set-up-ganche-with-metamask/?_x_tr_sl=en&_x_tr_tl=it&_x_tr_hl=it&_x_tr_pto=sc

