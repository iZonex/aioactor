import time
import ujson as json
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.utils import new_inbox
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def main():
    nc = NATS()
    data = {
        'user_id': 1
    }
    data = json.dumps(data).encode()
    await nc.connect()
    start_time = time.time()
    messages = 0
    inbox = new_inbox()
    while True:
        messages += 1
        try:
            response = await nc.publish_request("users.get", inbox, data)
        except ErrTimeout as err:
            print('Timeout')
        if time.time() - start_time > 1:
            print(messages)
            start_time = time.time()
            messages = 0



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
    loop.close()
