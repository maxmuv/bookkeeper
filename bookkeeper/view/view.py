from bookkeeper.view.abstract_view import AbstractView
from typing import Callable
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.view.expense_view import ExpenseView

from PySide6 import QtWidgets


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class View(AbstractView):
    def __init__(self, width: int, height: int, *args, **kwargs):
        self.window = MainWindow()
        self.window.setWindowTitle('The Bookkeeper App')
        self.window.resize(width, height)
        self.vbox = QtWidgets.QVBoxLayout()
        self.expense_view = ExpenseView()
        self.vbox.addWidget(self.expense_view)
        self.window.setLayout(self.vbox)

    def set_category_list(self, cat_list: list[str]) -> None:
        pass

    def set_budget(self, budget: list[int]) -> None:
        pass

    def set_expense_list(self, exp_list: list[list[str]]) -> None:
        self.expense_view.set_data(exp_list)

    def register_cat_modifier(self, handler: Callable[[Category], None]):
        pass

    def register_exp_modifier(self, handler: Callable[[Expense], None]):
        pass