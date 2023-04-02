from PySide6 import QtWidgets, QtCore, QtGui
from typing import Callable


class EditDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.add_del_menu = QtWidgets.QMenu(self)
        self.setWindowTitle("Категории")
        self.resize(300, 300)
        self.dlg_vbox = QtWidgets.QVBoxLayout()
        self.tree_view = QtWidgets.QTreeWidget()

        def set_cur_item(item, c):
            self.tree_view.setCurrentItem(item, c)
        self.tree_view.itemEntered.connect(set_cur_item)

        self.dlg_vbox.addWidget(self.tree_view)
        self.setLayout(self.dlg_vbox)
        self.adder_handler = None
        self.remove_handler = None
        self.name = ""
        self.current_item = ""

    def contextMenuEvent(self, event):
        self.add_del_menu.exec_(event.globalPos())

    def set_cat_adder_handler(self, handler: Callable[[str | None, str], None]):
        def func():
            item = self.tree_view.currentItem()
            name_widget = QtWidgets.QDialog()
            name_widget.setWindowTitle("Название")
            name_vbox = QtWidgets.QVBoxLayout()
            line = QtWidgets.QLineEdit()
            line.resize(50, 10)
            self.name = ""

            def get_name(text):
                self.name = text

            def finish_editing():
                name_widget.close()

            line.textChanged.connect(get_name)
            line.editingFinished.connect(finish_editing)
            name_vbox.addWidget(line)
            name_widget.setLayout(name_vbox)
            name_widget.exec()
            try:
                if item is None:
                    handler(None, self.name)
                else:
                    handler(item.text(self.tree_view.currentColumn()), self.name)
            except BaseException as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
            self.tree_view.setCurrentItem(self.tree_view.invisibleRootItem())
        self.adder_handler = func
        action = QtGui.QAction("Добавить",self.add_del_menu)
        action.triggered.connect(self.adder_handler)
        self.add_del_menu.addAction(action)

    def set_cat_remover_handler(self, handler: Callable[[str],None]):
        def func():
            item = self.tree_view.currentItem()
            try:
                if item is None:
                    handler(None)
                else:
                    handler(item.text(self.tree_view.currentColumn()))
            except BaseException as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
            self.tree_view.setCurrentItem(self.tree_view.invisibleRootItem())
        self.remove_handler = func
        action = QtGui.QAction("Удалить", self.add_del_menu)
        action.triggered.connect(self.remove_handler)
        self.add_del_menu.addAction(action)

    def register_handler(self, handler: Callable[[str, str], None]):
        def act_handler(item):
            self.current_item = item.text(0)

        def change_handler(item):
            try:
                handler(self.current_item, item.text(0))
            except BaseException as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
        self.tree_view.itemDoubleClicked.connect(act_handler)
        self.tree_view.itemChanged.connect(change_handler)


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
        self.dlg = EditDialog()

    def edit_button_clicked(self):
        self.dlg.exec()

    def set_data(self, cat: list[tuple[str, str | None]]) -> None:
        self.dlg.tree_view.clear()
        self.list_view.clear()
        self.dlg.tree_view.invisibleRootItem().setExpanded(True)
        cat_list = []
        node_list = {}
        for c_tuple in cat:
            child = QtWidgets.QTreeWidgetItem()
            child.setText(0, c_tuple[0])
            child.setExpanded(True)
            node_list[c_tuple[0]] = child
            cat_list.append(c_tuple[0])
            if c_tuple[1] is None:
                self.dlg.tree_view.invisibleRootItem().addChild(child)
            else:
                node_list[c_tuple[1]].addChild(child)
        self.list_view.addItems(cat_list)

    def register_handler(self, handler: Callable[[str, str], None]):
        self.dlg.register_handler(handler)

    def adder_handler(self, handler: Callable[[int, str], None]):
        def func():
            try:
                handler(int(self.line.text()), self.list_view.currentText())
            except BaseException as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
        self.sum_button.clicked.connect(func)

    def set_ctg_adder_handler(self, handler: Callable[[str, str], None]):
        self.dlg.set_cat_adder_handler(handler)

    def set_ctg_remover_handler(self, handler: Callable[[str], None]):
        self.dlg.set_cat_remover_handler(handler)
