"""
Services Broker
"""

from aioactor.transports import MessageTransport


class ServiceBroker:

    def __init__(self, **settings):
        self.logger = settings.get('logger')
        self.__message_transport = self.__setup_message_transport(
            settings.get('message_transport')
        )

    __services = {}

    def __setup_message_transport(self, message_transport):
        self.__message_transport = MessageTransport(
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
