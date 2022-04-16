import asyncio
from asyncio import sleep
from typing import List

import ntplib as ntplib
from httpx import AsyncClient

from account import Account


async def get(url, params={ }, headers={ }, cookies={ }):
    async with AsyncClient(headers=headers, cookies=cookies) as client:
        return await client.get(url, params=params)


async def post(url, json={ }, headers={ }, cookies={ }):
    async with AsyncClient(headers=headers, cookies=cookies) as client:
        return await client.post(url, json=json)


async def get_balance(account: Account):
    response = await post(
        "https://www.binance.com/bapi/nft/v1/private/nft/user-asset-board",
        { "assetList": ["BNB", "BUSD", "ETH"], "fiatName": "USD" }, account.headers, account.cookies
    )

    return response.json()


async def get_info(account: Account):
    response = await get(
        "https://www.binance.com/bapi/nft/v1/private/nft/user-info/simple-info", { }, account.headers, account.cookies
    )

    return response.json()


async def get_box_info(product_id: int, account: Account):
    response = await get(
        f"https://www.binance.com/bapi/nft/v1/friendly/nft/mystery-box/detail", { 'productId': product_id },
        account.headers, account.cookies
    )

    return response.json()


async def get_product_details(product_id: int, account: Account):
    response = await post(
        f"https://www.binance.com/bapi/nft/v1/friendly/nft/nft-trade/product-detail", { 'productId': product_id },
        account.headers, account.cookies
    )

    return response.json()


async def order_good(product: dict, account: Account):
    response = await post(
        f"https://www.binance.com/bapi/nft/v1/private/nft/nft-trade/order-create", {
            "amount"   : product['data']['productDetail']['amount'],
            "productId": product['data']['productDetail']['id'], "tradeType": 0
        }, account.headers, account.cookies
    )

    return response.json()


async def confirm_order(order: dict, account: Account):
    response = await post(
        f"https://www.binance.com/bapi/nft/v1/private/nft/nft-trade/order-query", {
            { "orderNo": order['data']['requestId'], "tradeType": 1 }, account.headers, account.cookies
        }
    )

    return response.json()


async def buy_box(product_id: int, count: int, account: Account):
    try:
        response = await post(
            "https://www.binance.com/bapi/nft/v1/private/nft/mystery-box/purchase",
            { "number": count, "productId": product_id },
            account.headers,
            account.cookies
        )

        return response.json()
    except Exception as e:
        return e


async def main(accounts: List[Account]):
    # a = accounts[0]
    # print(await get_box_info(133913760132809728, a))
    # exit(0)

    # for account in accounts:
    #     info = (await get_info(account))['data']
    #     balances = (await get_balance(account))['data']['assetBalanceList']
    #     print(f"{info['nickName'] or info['userId']}: ${balances[0]['total'] if balances else 0}")

    account = accounts[0]

    details = await get_product_details(45709914, account)
    print(details)

    await sleep(5)

    order = await order_good(details, account)
    print(order)

    await sleep(5)

    confirmation = await confirm_order(order, account)
    print(confirmation)

    #
    #
    # box = 208933749931879424
    # buy_count = 3
    #
    # ntp = ntplib.NTPClient()
    # global_time = ntp.request("asia.pool.ntp.org", version=3).tx_time * 1000
    # box_start_time = (await get_box_info(box, account))  # ['data']['startTime']
    #
    # print((await get_balance(account)))  # ['data']['assetBalanceList'])

    # while global_time - 1200 < box_start_time:
    #     print(int(box_start_time - global_time) / 1000, "сек")
    #     global_time = ntp.request("asia.pool.ntp.org", version=3).tx_time * 1000
    #
    #     await asyncio.sleep(0.1)
    #
    # while True:
    #     if any(
    #             [x['success'] for x in await asyncio.gather(
    #                 *[buy_box(box, buy_count, account),
    #                   buy_box(box, buy_count, account),
    #                   buy_box(box, buy_count, account),
    #                   buy_box(box, buy_count, account),
    #                   buy_box(box, buy_count, account),
    #                   buy_box(box, buy_count, account)]
    #             )]
    #     ):
    #         print(f"{buy_count} boxes bought")
    # print(datetime.fromtimestamp(data.json()['data']['startTime'] / 1000) - datetime.now())


if __name__ == '__main__':
    b = Account("ce2dc6ee02c419789e560d59260a1f92", "web.23898099.23AF1687A5E57794896DB981C4D15C33")
    # a = Account("0fa7e5e2eea71ae9d6e92823fbf308df", "web.216186886.9684B9B09B666F01120D2617B2656359")

    asyncio.run(
        main([b])
    )
