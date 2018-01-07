import yaml
import argparse

# TODO Detect file type json or yaml
# TODO Create arguments help menu
# TODO Get file structure

class BaseGenerator:

    pass

class ServerGenerator(BaseGenerator):

    def __init__(self, file_path):
        self.file_path = file_path

    def generate(self):
        print(file_path)

class ClientGenerator(BaseGenerator):

    def __init__(self, file_path):
        self.file_path = file_path

    def generate(self):
        print(file_path)

class ModuleGenerator(BaseGenerator):

    def __init__(self, file_path):
        self.file_path = file_path

    def generate(self):
        print(file_path)

class ApplicationGenerator:

    def __init__(self, app_generator, file_path, destination=None):
        self.app_generator = app_generator(file_path)

    def create(self):
        self.app_generator.generate()

def main():
    if args.generate == 'client':
        app_generator = ClientGenerator
    elif args.generate == 'server':
        app_generator = ServerGenerator
    elif args.generate == 'module':
        app_generator = ModuleGenerator
    app_gen = ApplicationGenerator(app_generator, file_path, destination)
    app_gen.create()


if __name__ == '__main__':

    instruction = """
    aioactor starter application generator
    """
    parser = argparse.ArgumentParser(instruction)
    parser.add_argument(
        "-g",
        "--generate",
        choices=['client', 'server', 'module'],
        type=str,
        help="Choice generation task type",
        default='server')
    parser.add_argument("file", help="file location")
    parser.add_argument("destination", help="application destination")
    args = parser.parse_args()
    file_path = args.file
    destination = args.destination
    main(app_generator, file_path, destination)