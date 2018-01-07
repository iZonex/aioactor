import time
import asyncio
import uvloop
from aioactor.transports import NatsTransport
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# TODO ADD possible actions list!
# TODO ADD abstractions to Message Handler!
# MessageHandler must be able to call methods of Service and control requests

class MessageHandler:

    def __init__(self, handler_type, subscribe_list, call_service):
        self.handler = handler_type.get('handler')(subscribe_list, call_service)

    async def run(self):
        await self.handler.subscribe()


class ServiceBroker:

    def __init__(self, **settings):
        self.logger = settings.get('logger')
        self.__message_transport = self.__setup_message_transport(
            settings.get('message_transport')
        )

    __services = {}

    def __setup_message_transport(self, message_transport):
        self.__message_transport = MessageHandler(
            message_transport, self.__services, self.call_service)

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
        await self.__message_transport.run()


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


async def main():
    settings = {
        'logger': 'console',
        'message_transport': {
            'handler': NatsTransport
        }
    }
    broker = ServiceBroker(io_loop=loop, **settings)
    broker.create_service(Users())
    print(broker.available_services())
    await broker.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
    loop.close()
