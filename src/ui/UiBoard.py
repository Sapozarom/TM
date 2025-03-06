
from src.obj.BoardField import BoardField
from PyQt5.QtCore import QEvent
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap


class UiBoard(QtWidgets.QWidget):
    """UI part \n
    represent full board with all fields and their attributes"""

    fields = []

    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(1000, 800)

        # dimension must be multiplication of 4
        self.field_dimension = 76
        self.board_width = 800
        self.board_height = int(
            9 * self.field_dimension * 0.75 + self.field_dimension * 0.25)

        self.fields_in_row = [5, 6, 7, 8, 9, 8, 7, 6, 5]

        self.create_board_frame()

        self.draw_raws()

        # print(len(self.fields[0]))

    def create_board_frame(self):

        self.board_frame = QtWidgets.QFrame(self)
        self.board_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.board_frame.setGeometry(
            100, 100, self.board_width, self.board_height)

    def create_board_field(self, x, y, row_tilt):

        field = QtWidgets.QLabel(self.board_frame)
        field.move(row_tilt+x, y)
        field.setFixedSize(self.field_dimension, self.field_dimension)
        field.setStyleSheet("padding : 1px;")
        field.installEventFilter(self)
        image = QPixmap("hex.png")
        field.setPixmap(image)
        field.setScaledContents(True)
        field.show()
        return field

    def eventFilter(self, object, event):
        image = QPixmap("hex.png")
        image_hover = QPixmap("hex_clicked.png")
        if event.type() == QEvent.Enter:
            object.setPixmap(image_hover)
            print(object.objectName())
            return True
        elif event.type() == QEvent.Leave:
            object.setPixmap(image)
        return False

    def draw_raws(self):
        row_number = 0

        for fields in self.fields_in_row:
            row = []
            x_cord = 0
            y_cord = int(
                row_number * self.field_dimension * 0.75)
            row_tilt = int(
                (self.board_width - self.field_dimension * fields) * 0.5)

            for x in range(fields):
                field_label = self.create_board_field(x_cord, y_cord, row_tilt)
                cords = f"{row_number},{x}"
                field_label.setObjectName("fl_"+cords)
                new_field = BoardField(x_cord, y_cord, field_label)
                row.append(new_field)
                x_cord += self.field_dimension

            self.fields.append(row)
            row_number += 1
