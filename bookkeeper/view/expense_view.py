from PySide6 import QtWidgets
from bookkeeper.models.expense import Expense
from inspect import get_annotations


class ExpenseView(QtWidgets.QTableWidget):
    def __init__(self):
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

    def set_data(self, expenses: list[list[str]]):
        self.setRowCount(len(expenses))
        for i, row in enumerate(expenses):
            for j, x in enumerate(row):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(x.capitalize())
)