from PySide6 import QtWidgets, QtGui
from typing import Callable


class ExpenseView(QtWidgets.QTableWidget):
    def __init__(self) -> None:
        super().__init__(0, 4)
        self.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split())

        header = self.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)

        self.handler = lambda item: None
        self.is_item_clicked = False
        self.del_menu = QtWidgets.QMenu(self)
        self.remove_handler = None

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        self.del_menu.exec_(event.globalPos())

    def set_data(self, expenses: list[list[str]]) -> None:
        self.setRowCount(len(expenses))
        for i, row in enumerate(expenses):
            for j, x in enumerate(row):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(x.capitalize()))

    def set_handler(self, handler: Callable[[int, int, str], None]) -> None:
        def func(item: QtWidgets.QTableWidgetItem) -> None:
            if not self.is_item_clicked:
                return
            self.is_item_clicked = False
            r = item.row()
            c = item.column()
            s = item.text()
            try:
                handler(r, c, s)
            except BaseException as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))

        def func1() -> None:
            self.is_item_clicked = True

        self.handler = func
        self.itemChanged.connect(self.handler)
        self.itemDoubleClicked.connect(func1)

    def set_del_menu(self, handler: Callable[[int], None]) -> None:
        def func() -> None:
            row = self.currentItem().row()
            try:
                handler(row)
            except BaseException as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
        self.remove_handler = func
        action = QtGui.QAction("Удалить", self.del_menu)
        action.triggered.connect(self.remove_handler)
        self.del_menu.addAction(action)
