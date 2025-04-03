import sys

from src.lib.createDbTables.createDbTables import CreateDbTables
from src.lib.updateDbConst.updateDbConst import UpdateDbConst


def main():
    model = CreateDbTables()
    model.main()

    const = UpdateDbConst()
    const.main()


if __name__ == "__main__":
    main()
