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
        self.list_view = QtWidgets.QComboBox()
        self.vbox.addWidget(self.list_view, 1, 1)
        self.edit_button = QtWidgets.QPushButton("Редактировать")
        self.edit_button.clicked.connect(self.edit_button_clicked)
        self.vbox.addWidget(self.edit_button, 1, 2)
        self.sum_button = QtWidgets.QPushButton("Добавить")
        self.vbox.addWidget(self.sum_button, 2, 1)
        self.setLayout(self.vbox)
        self.dlg = QtWidgets.QDialog(self)
        self.dlg.setWindowTitle("Категории")
        self.dlg.resize(300, 300)
        self.dlg_vbox = QtWidgets.QVBoxLayout()
        self.tree_view = QtWidgets.QTreeView()
        self.dlg_vbox.addWidget(self.tree_view)
        self.dlg.setLayout(self.dlg_vbox)

    def edit_button_clicked(self):
        self.dlg.exec()

