from functools import partial


class ServiceBroker:

    def __init__(self, **settings):
        self.logger = settings.get('logger')

    __services = []

    def create_service(self, service):
        self.__services.append(service)

    def start(self):
        pass
        # for i in self.__services:
        #     print(i.name)


def action(name=None):

    print(f"Action with name: {name} was added")

    def real_decorator(function):
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator


class Service:
    pass


class Math(Service):

    name = "math"

    @action("add")
    def add(self, x: int, y: int) -> int:
        return x + y


def main():
    settings = {'logger': 'console'}
    broker = ServiceBroker(**settings)
    broker.create_service(Math)
    broker.start()

if __name__ == '__main__':
    main()
