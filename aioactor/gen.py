import yaml
import argparse

# TODO Detect file type json or yaml
# TODO Create arguments help menu
# TODO Get file structure

class Generator:
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--foo', help='foo help')
    args = parser.parse_args()
