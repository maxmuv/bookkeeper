from bookkeeper.view.abstract_view import AbstractView
from typing import Callable
from bookkeeper.view.expense_view import ExpenseView
from bookkeeper.view.budget_view import BudgetView
from bookkeeper.view.category_view import CategoryView
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
        expense_msg = QtWidgets.QLabel("Последние расходы")
        self.expense_view = ExpenseView()
        self.vbox.addWidget(expense_msg)
        self.vbox.addWidget(self.expense_view)
        budget_msg = QtWidgets.QLabel("Бюджет")
        self.budget_view = BudgetView()
        self.vbox.addWidget(budget_msg)
        self.vbox.addWidget(self.budget_view)
        self.category_view = CategoryView()
        self.vbox.addWidget(self.category_view)
        self.window.setLayout(self.vbox)

    def set_category_list(self, cat_list: list[str]) -> None:
        pass

    def set_budget(self, budget: list[list[int]]) -> None:
        self.budget_view.set_data(budget)

    def set_expense_list(self, exp_list: list[list[str]]) -> None:
        self.expense_view.set_data(exp_list)

    def register_cat_modifier(self, handler: Callable[[int], None]):
        pass

    def register_exp_modifier(self, handler: Callable[[int, int, str], None]):
        self.expense_view.set_handler(handler)

    def register_budget_modifier(self, handler: Callable[[int, int, str], None]):
        self.budget_view.register_handler(handler)
