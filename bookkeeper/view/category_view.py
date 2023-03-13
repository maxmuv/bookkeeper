from PySide6 import QtWidgets


class CategoryView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QtWidgets.QGridLayout()
        self.sum_label = QtWidgets.QLabel("Сумма")
        self.vbox.addWidget(self.sum_label, 0, 0)
        self.line = QtWidgets.QLineEdit()
        self.vbox.addWidget(self.line, 0, 1)
        self.cat_label = QtWidgets.QLabel("Категории")
        self.vbox.addWidget(self.cat_label, 1, 0)
        self.tree = QtWidgets.QComboBox()
        self.vbox.addWidget(self.tree, 1, 1)
        self.edit_button = QtWidgets.QPushButton("Редактировать")
        self.vbox.addWidget(self.edit_button, 1, 2)
        self.sum_button = QtWidgets.QPushButton("Добавить")
        self.vbox.addWidget(self.sum_button, 2, 1)
        self.setLayout(self.vbox)
