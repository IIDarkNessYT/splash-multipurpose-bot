import json
import secrets
import string
import asyncio
import os
import shutil
import aiohttp


def load_json(filename):
    with open(filename, encoding="utf-8") as infile:
        return json.load(infile)


def write_json(filename, content):
    with open(filename, "w") as outfile:
        json.dump(content, outfile, ensure_ascii=True, indent=4)


bot = load_json("configs/config.json")


class request():

    @classmethod
    async def post(self, url, content, headers=None):
        async with aiohttp.ClientSession() as call:
            if content is not None:
                if headers is not None:
                    async with call.request(method='POST', url=url, data=content, headers=headers) as response:
                        return json.loads(await response.text())
                else:
                    async with call.request(method='POST', url=url, data=content) as response:
                        return json.loads(await response.text())
            else:
                if headers is not None:
                    async with call.request(method='POST', url=url, headers=headers) as response:
                        return json.loads(await response.text())
                else:
                    async with call.request(method='POST', url=url) as response:
                        return json.loads(await response.text())


def generate_password(length):
    password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(length)))
    return password


async def check_premium(guild, owner):
    jsonstr = {
        "guild": f"{guild}",
        "owner": f"{owner}",
        "buyed_by": "СИСТЕМА",
        "type": "get"
    }
    
    url = f"API URL"
    result = await request.post(url, jsonstr)
    if result['status'] == 'true':
        return True
    else:
        return False


def check_bot_owner(user):
    if int(user) in bot['owners']:
        return True
    else:
        return False
