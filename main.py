import sys

from src.ui.UiBoard import UiBoard
from PyQt5 import QtWidgets

from src.service.createDbTables.CreateDbTables import CreateDbTables


def main():
    db = CreateDbTables()

    app = QtWidgets.QApplication(sys.argv)
    b = UiBoard()
    b.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
