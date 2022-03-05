
from web3 import Web3

from scripts.helpful_scripts import get_account
from brownie import  interface,config,network

def convert_to_WETH_or_WAVAX():
    #Address
    account=get_account()
    #ABI
    if network.show_active() in ["avax-main-fork","avax-main","avax-test"]:
        weth=interface.IWavax(config["networks"][network.show_active()]["wavax_token"])
        tx=weth.deposit({"from":account,"value": 0.1 * 10 ** 18})
    else:
        weth=interface.IWeth(config["networks"][network.show_active()]["weth_token"])
        tx=weth.deposit({"from":account,"value": 0.1 * 10 ** 18})
    tx.wait(1)
    print("wETH recieved")
    return tx

def main():
    convert_to_WETH_or_WAVAX()
