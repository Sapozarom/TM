import sys

from src.service.parser.parser import Parser


def main():
    parser = Parser()
    parser.read_lines()


if __name__ == "__main__":
    main()
