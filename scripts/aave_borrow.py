from web3 import Web3
from scripts.helpful_scripts import  get_account,LOCAL_DEVELOPMENT_ENVS
from scripts.get_weth import convert_to_WETH
from brownie import network ,config,interface
def amt():
    print("enter Amount in ETH: \n")
    amount=Web3.toWei(input(),"ether")
    at=Web3.fromWei(amount,"ether")
    print(f"\nUr amount in Wei is: {at}")
    return amount

def main():
    account=get_account()
    erc20_address=config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        convert_to_WETH()
    lending_pool=get_lending_pool()
    print(lending_pool.address)
    AMT=amt()

    approve_erc20(AMT,lending_pool.address,erc20_address,account)

    print("\nDepositing....\n")
    tx=lending_pool.deposit(erc20_address,AMT,account.address,0,{"from":account})
    tx.wait(1)
    print("\nDeposited\n")





def approve_erc20(value,spender,erc20_address,account):
    print("Approving....")
    erc20=interface.IERC20(erc20_address)
    tx=erc20.approve(spender,value,{"from":account})
    tx.wait(1)
    print("APPROVED")
    return tx 





def get_lending_pool():
    Lending_Pool_Addresses_Provider=interface.ILendingPoolAddressesProvider(config["networks"][network.show_active()]["lending_pool_addresses_provider"])
    Lending_Pool_Address=Lending_Pool_Addresses_Provider.getLendingPool()
    Lending_Pool= interface.ILendingPool(Lending_Pool_Address)
    return Lending_Pool
        
