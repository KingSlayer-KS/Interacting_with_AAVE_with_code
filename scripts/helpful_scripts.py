from brownie import network, accounts, config

FORKED_ENVS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_DEVELOPMENT_ENVS = [
    "mainnet-fork",
    "development",
    "Ganache-local",
]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_DEVELOPMENT_ENVS:
        return accounts[0]
    # if nothing above 3 statmens is true the below one will be done
    return accounts.add(config["wallets"]["from_key"])
