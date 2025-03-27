import sys

from src.lib.createDbTables.CreateDbTables import CreateDbTables


def main():
    model = CreateDbTables()
    model.main()


if __name__ == "__main__":
    main()
