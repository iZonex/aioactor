import asyncio
import uvloop
from aioactor.transports import NatsTransport
from aioactor.service import Service
from aioactor.broker import ServiceBroker
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# TODO ADD possible actions list!
# TODO ADD abstractions to Message Handler!
# MessageHandler must be able to call methods of Service and control requests
# TODO Aggregate date about user [userinfo, location, photo]


class UsersService(Service):

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

# TODO Add protected types for registration
# TODO Add protocols accepted types for services


def register_services(broker, services):
    for service in services:
        broker.create_service(service())


async def main():
    settings = {
        'logger': 'console',
        'message_transport': {
            'handler': NatsTransport
        }
    }
    broker = ServiceBroker(io_loop=loop, **settings)
    services = [UsersService]
    register_services(broker, services)
    print(broker.available_services())
    await broker.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
    loop.close()
