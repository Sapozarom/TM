import sys

from src.lib.database.createDbTables.createDbTables import CreateDbTables
from src.lib.database.updateDbConst.updateDbConst import UpdateDbConst


def main():
    model = CreateDbTables()
    model.main()

    const = UpdateDbConst()
    const.main()


if __name__ == "__main__":
    main()
