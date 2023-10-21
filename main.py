# -*- coding: utf-8 -*-
import os
import random
from collections import Counter

import asyncio
import aiohttp
from aiohttp_proxy import ProxyConnector
from fake_useragent import UserAgent
from tabulate import tabulate


async def meme_request(token, connector, result_dict, num, depth=10):
    if depth == 0:
        print(f"Error: token number {num + 1} in tokens.txt has an error")
        if not os.path.exists('failed_tokens.txt'):
            with open('failed_tokens.txt', 'w') as f:
                f.write("Number token of tokens.txt, Token\n")
        with open('failed_tokens.txt', 'a') as f:
            f.write(f"{num + 1}, {token}\n")
        return

    user_agent = UserAgent().chrome
    version = user_agent.split("Chrome/")[1].split(".")[0]
    platform = ["macOS", "Windows", "Linux"]

    headers = {
    'authority': 'memefarm-api.memecoin.org',
    'accept': 'application/json',
    'accept-language': 'ru-RU,ru;q=0.9,uk;q=0.8',
    'authorization': token,
    'origin': 'https://www.memecoin.org',
    'referer': 'https://www.memecoin.org/',
    'sec-ch-ua': f'"Chromium";v="{version}", "Google Chrome";v="{version}", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': f'"{random.choice(platform)}"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': user_agent,
}

    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with await session.get(
                url="https://memefarm-api.memecoin.org/user/info",
                headers=headers
            ) as r:
                result = await r.json()
                if result["inviteCode"]:
                    result_dict[result["inviteCode"]] = result_dict.get(result["inviteCode"], 0) + 1
    except (KeyError, RuntimeError) as err:
        await meme_request(token, connector, result_dict, num, depth - 1)
    except aiohttp.ClientError:
        pass


async def start_request(tokens_list, proxys_list, result_dict):
    if proxys_list:
        proxy_connectors = [ProxyConnector.from_url(proxy) for proxy in proxys_list[:len(tokens_list)]]
    else:
        proxy_connectors = [None] * len(tokens_list)

    tasks = [asyncio.create_task(meme_request(token, proxy_connectors[i], result_dict, i)) for i, token in enumerate(tokens_list)]
    await asyncio.wait(tasks)


def read_list_from_txt(file_name):
    with open(file_name, "r") as file:
        return [line.strip() for line in file]


def main():
    tokens_list = read_list_from_txt("tokens.txt")
    unique_tokens_dict = Counter(tokens_list)

    proxys_list = read_list_from_txt("proxys.txt")
    result_dict = {}

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_request(tokens_list, proxys_list, result_dict))
    
    result = []
    

    for key, value in result_dict.items():
        result.append([str(key), str(value)])

    tokens = ["Tokens in tokens.txt", len(tokens_list)]
    result.append(tokens)
    unique_tokens = ["Unique tokens", len(unique_tokens_dict)]
    result.append(unique_tokens)
    headers = ["InviteCode", "Count Result"]
    table = tabulate(result, headers, tablefmt="grid")
    print(table)

if __name__ == "__main__":
    main()
