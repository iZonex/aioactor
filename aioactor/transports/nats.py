import time
import ujson as json
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


class NatsTransport:

    def __init__(self, subscribe_list, call_service):
        self.start_time = time.time()
        self.messages_total = 0
        self.subscribe_list = subscribe_list
        self.call_service = call_service
        self.loop = asyncio.get_event_loop()
        self.nc = NATS()

    async def message_handler(self, msg):
        self.messages_total += 1
        if time.time() - self.start_time > 1:
            print(self.messages_total)
            self.start_time = time.time()
            self.messages_total = 0
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        # print("Received a message on '{subject} {reply}': {data}".format(
        #     subject=subject, reply=reply, data=data))
        data = json.loads(data)
        result = await self.call_service(subject, **data)
        dumped = json.dumps({"result": result})
        await self.nc.publish(reply, dumped.encode())

    async def subscribe(self):
        await self.nc.connect(io_loop=self.loop)
        for service_key in self.subscribe_list.keys():
            await self.nc.subscribe_async(
                f"{service_key}",
                cb=self.message_handler)

    async def publish(self, topic, inbox, data):
        response = await nc.publish_request("users.get", inbox, data)
        return response
