"""
Base of the message transport abstraction
"""

class MessageTransport:

    def __init__(self, handler_type, subscribe_list, call_service):
        self.handler = handler_type.get('handler')(subscribe_list, call_service)

    async def run(self):
        await self.handler.subscribe()