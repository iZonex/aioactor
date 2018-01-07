import json
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

# TODO ADD possible actions list!
# TODO ADD abstractions to Message Handler!
# MessageHandler must be able to call methods of Service and control requests

class NatsHandler:

    def __init__(self, subscribe_list, call_service):
        self.subscribe_list = subscribe_list
        self.call_service = call_service
        self.loop = asyncio.get_event_loop()
        self.nc = NATS()

    async def message_handler(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        data = json.loads(data)
        result = await self.call_service(subject, **data)
        dumped = json.dumps({"result": result})
        await self.nc.publish(reply, dumped.encode())

    async def subscribe(self):
        await self.nc.connect(io_loop=self.loop)
        for service_key in self.subscribe_list.keys():
            await self.nc.subscribe(f"{service_key}", cb=self.message_handler)

class MessageHandler:

    def __init__(self, handler_type, subscribe_list, call_service):
        self.handler = handler_type.get('handler')(subscribe_list, call_service)

    async def run(self):
        await self.handler.subscribe()


class ServiceBroker:

    def __init__(self, **settings):
        self.logger = settings.get('logger')
        self.message_handler = MessageHandler(settings.get(
            'message_handler'), self.__services, self.call_service)

    __services = {}

    def create_service(self, service):
        for action_name, action_method in service.actions.items():
            service_name = f"{service.name}.{action_name}"
            self.__services.setdefault(service_name, action_method)

    def available_services(self):
        return self.__services

    async def call_service(self, name, *args, **kwargs):
        try:
            result = await self.__services.get(name)(*args, **kwargs)
        except Exception as err:
            print(f'error {err}')
        return result

    async def start(self):
        await self.message_handler.run()


class Service:

    name = None
    actions = {}


class Users(Service):

    def __init__(self):
        self.name = "users"
        self.actions = {
            'get': self.get_user_name
        }

    async def get_user_name(self, user_id: int) -> dict:
        users = {
            1: {
                'firstname': 'Antonio',
                'lastname': 'Rodrigas'
            }
        }
        user_obj = users.get(user_id, {})
        return user_obj


async def main(loop):
    settings = {
        'logger': 'console',
        'message_handler': {
            'handler': NatsHandler
        }
    }
    broker = ServiceBroker(io_loop=loop, **settings)
    broker.create_service(Users())
    print(broker.available_services())
    await broker.start()
    nc = NATS()
    data = {
        'user_id': 1
    }
    await nc.connect()
    response = await nc.timed_request("users.get", json.dumps(data).encode(), 0.050)
    print('response:', response.data.decode())



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_forever()
    loop.close()
