
class ServiceBroker:

    def __init__(self, **settings):
        self.logger = settings.get('logger')

    __services = {}

    def create_service(self, service):
        for action_name, action_method in service.actions.items():
            service_name = f"{service.name}.{action_name}"
            self.__services.setdefault(service_name, action_method)

    def available_services(self):
        return self.__services

    def call_service(self, name, *args, **kwargs):
        try:
            result = self.__services.get(name)(*args, **kwargs)
        except Exception as err:
            print(f'error {err}')
        return result

    def start(self):
        pass


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
    print(broker.available_services())
    print(broker.call_service('math.sumadd', 6, 5))

if __name__ == '__main__':
    main()
