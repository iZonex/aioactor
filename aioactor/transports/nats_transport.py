import ujson as json
import asyncio
from nats.aio.client import Client
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

# TODO connect to init!
# TODO Added Handle for server interuptions
# TODO replace json dumps to serializer

class NatsTransport:

    def __init__(self, subscribe_list, call_service):
        self.__subscribe_list = subscribe_list
        self.__call_service = call_service
        self.__loop = asyncio.get_event_loop()
        self.__client = Client()

    async def __message_handler(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        data = json.loads(data)
        result = await self.__call_service(subject, **data)
        print(result)
        # dumped = json.dumps({"result": result})
        # await self.client.publish(reply, dumped.encode())

    async def subscribe(self):
        await self.__client.connect(io_loop=self.__loop)
        for service_key in self.__subscribe_list.keys():
            await self.__client.subscribe_async(
                f"{service_key}",
                cb=self.__message_handler)

    async def publish(self, topic, inbox, data):
        await self.__client.connect(io_loop=self.__loop)
        response = await self.__client.publish_request(topic, inbox, data)
        return response
