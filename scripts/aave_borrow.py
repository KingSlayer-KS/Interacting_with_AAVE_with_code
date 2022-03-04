from web3 import Web3
from scripts.helpful_scripts import get_account, LOCAL_DEVELOPMENT_ENVS
from scripts.get_weth import convert_to_WETH
from brownie import network, config, interface


def amt():
    print("Enter Amount in ETH: ")
    amo = input()
    amount = Web3.toWei(amo, "ether")
    print(f"\nUr amount in Wei is: {amount}")
    return amount


def get_asset_price(price_feed_address):
    dai_eth_pricefeed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_pricefeed.latestRoundData()[1]
    latest_pricefeed_in_eth = Web3.fromWei(latest_price, "ether")
    print(f"Dai/ETH pricefeed is: {latest_pricefeed_in_eth}\n")
    return float(latest_pricefeed_in_eth)


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)

    print("Repaid!")


def get_borrowable_data(lending_pool, account):
    (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowsETH,
        currentLiquidationThreshold,
        ltv,  # liquadiation_to_valuer_ratio
        healthFactor,
    ) = lending_pool.getUserAccountData(account.address)
    availableBorrowsETH = Web3.fromWei(availableBorrowsETH, "ether")
    totalCollateralETH = Web3.fromWei(totalCollateralETH, "ether")
    totalDebtETH = Web3.fromWei(totalDebtETH, "ether")
    print(f"u have {totalCollateralETH} worth ETH deposited")
    print(f"u have {totalDebtETH} worth ETH debt")
    print(f"u have {availableBorrowsETH} worth ETH u can borrow\n")
    return (float(availableBorrowsETH), float(totalDebtETH))


# amount, address_of_lending_pool_contract, ERC-20_token_address, Account_selected
def approve_erc20(value, spender, erc20_address, account):
    print("Approving....")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, value, {"from": account})
    tx.wait(1)
    print("APPROVED")
    return tx


def get_lending_pool():
    Lending_Pool_Addresses_Provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    Lending_Pool_Address = Lending_Pool_Addresses_Provider.getLendingPool()
    Lending_Pool = interface.ILendingPool(Lending_Pool_Address)
    return Lending_Pool


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        convert_to_WETH()
    lending_pool = get_lending_pool()
    print(lending_pool.address)
    AMT = amt()
    approve_erc20(AMT, lending_pool.address, erc20_address, account)

    print("\nDepositing....\n")
    tx = lending_pool.deposit(erc20_address, AMT, account.address, 0, {"from": account})
    tx.wait(1)
    print("\nDeposited\n")
    borrowable_ETH, total_debt = get_borrowable_data(lending_pool, account)

    print("Lets_borrow\n")
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    borrow_dai = (1 / dai_eth_price) * (borrowable_ETH * 0.95)
    # borrowable_ETH=>borrowable_DAI
    # 95%of_borrowable_amount=oborrowable_amount/0.95
    """
    make sure the amount u borrow is aleays less then the ur maximum borrowable amoumt
    thsi implies that th 0.95 can alsio be 0.5"""
    print(f"We are goin to borrow: {borrow_dai}  DAI\n")
    # Now we will borrow!
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,  # address assetuint256 amount
        Web3.toWei(borrow_dai, "ether"),  # int256 amount
        1,  # uint256 interestRateMode[1=stable,0=varriable]
        0,  # uint16 referralCode(always_zero)
        account.address,  # address onBehalfOf
        {"from": account},
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI!\n")
    get_borrowable_data(lending_pool, account)
    repay_all(Web3.toWei(borrow_dai, "ether"), lending_pool, account)
    get_borrowable_data(lending_pool, account)
    print(
        "You just deposited, borrowed, and repayed with Aave, Brownie, and Chainlink!"
    )
