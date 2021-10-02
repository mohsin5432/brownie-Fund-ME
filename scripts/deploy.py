from brownie import FundMe, MockV3Aggregator, network, config, accounts
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000

FORKED_LOCAL_ENVOIRMENTS = ["mainnet-fork", "mainnet-fork-dev"]

LOCAL_BLOCKCHAIN_ENVOIRMENT = ["development", "ganache-local"]


def deploy_fund_me():
    account = get_account()
    # pass price feed address
    # if we are on rinkeby we will use this associated address
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVOIRMENT:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": account})
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print("Contract diployed to " + fund_me.address)
    return fund_me


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVOIRMENT
        or network.show_active() in FORKED_LOCAL_ENVOIRMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_fund_me()
