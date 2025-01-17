from PySide6 import QtWidgets, QtCore
from typing import Callable


class BudgetView(QtWidgets.QTableWidget):
    def __init__(self) -> None:
        super().__init__(3, 2)
        self.setHorizontalHeaderLabels(
            "Сумма Бюджет".split())
        self.setVerticalHeaderLabels(
            "День Неделя Месяц".split())
        self.handler = lambda item: None

    def set_data(self, data: list[list[int]]) -> None:
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(x).capitalize())
                if j == 0:
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i, j, item)

    def register_handler(self, handler: Callable[[int, int, str], None]) -> None:
        def func(item):
            r = item.row()
            c = item.column()
            i = item.text()
            try:
                handler(r, c, i)
            except BaseException as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
        self.handler = func
        self.itemChanged.connect(self.handler)
