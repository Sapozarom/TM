import sys

from src.service.createDbTables.CreateDbTables import CreateDbTables


def main():
    model = CreateDbTables()
    model.main()


if __name__ == "__main__":
    main()
