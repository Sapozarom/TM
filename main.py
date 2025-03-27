import sys

from src.ui.uiBoard import UiBoard
from PyQt5 import QtWidgets

from src.lib.createDbTables.CreateDbTables import CreateDbTables


def main():
    db = CreateDbTables()

    app = QtWidgets.QApplication(sys.argv)
    b = UiBoard()
    b.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
