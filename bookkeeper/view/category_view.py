from PySide6 import QtWidgets, QtCore, QtGui
from typing import Callable


class CategoryView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QtWidgets.QGridLayout()
        self.sum_label = QtWidgets.QLabel("Сумма")
        self.vbox.addWidget(self.sum_label, 0, 0)
        self.line = QtWidgets.QLineEdit()
        only_int = QtGui.QIntValidator()
        only_int.setRange(0, 999999)
        self.line.setValidator(only_int)
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
        self.tree_view = QtWidgets.QTreeWidget()
        self.dlg_vbox.addWidget(self.tree_view)
        self.dlg.setLayout(self.dlg_vbox)
        self.current_item = ""

    def edit_button_clicked(self):
        self.dlg.exec()

    def set_data(self, cat: list[tuple[str, str | None]]) -> None:
        self.tree_view.invisibleRootItem().setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
        self.tree_view.invisibleRootItem().setExpanded(True)
        cat_list = []
        node_list = {}
        for c_tuple in cat:
            child = QtWidgets.QTreeWidgetItem()
            child.setText(0, c_tuple[0])
            child.setExpanded(True)
            child.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            node_list[c_tuple[0]] = child
            cat_list.append(c_tuple[0])
            if c_tuple[1] is None:
                self.tree_view.invisibleRootItem().addChild(child)
            else:
                node_list[c_tuple[1]].addChild(child)
        self.list_view.addItems(cat_list)

    def register_handler(self, handler: Callable[[str, str], None]):
        def act_handler(item):
            self.current_item = item.text(0)
            print(self.current_item)

        def change_handler(item):
            handler(self.current_item, item.text(0))
        self.tree_view.itemDoubleClicked.connect(act_handler)
        self.tree_view.itemChanged.connect(change_handler)

    def adder_handler(self, handler: Callable[[int, str],None]):
        def func():
            handler(int(self.line.text()), self.list_view.currentText())
        self.sum_button.clicked.connect(func)
