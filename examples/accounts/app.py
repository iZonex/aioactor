class ServiceBroker:

    def __init__(self, **settings):
        self.logger = settings.get('logger')

    __services = []

    def create_service(self, service):
        self.__services.append(service)

    def start(self):
        for i in self.__services:
            print(i.name)
            print(i.actions)


class Service:

    name = None
    actions = {}


class Math(Service):

    def __init__(self):
        self.name = "math"
        self.actions = {
            'sumadd': self.add
        }

    def add(self, x: int, y: int) -> int:
        return x + y


def main():
    settings = {'logger': 'console'}
    broker = ServiceBroker(**settings)
    broker.create_service(Math())
    broker.start()

if __name__ == '__main__':
    main()
