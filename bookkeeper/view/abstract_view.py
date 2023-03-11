from typing import Protocol, Callable
from abc import abstractmethod
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from PySide6 import QtWidgets


class AbstractView(Protocol):
    @abstractmethod
    def set_category_list(self, cat_list: list[str]) -> None:
        pass

    @abstractmethod
    def set_budget(self, budget: list[int]) -> None:
        pass

    @abstractmethod
    def set_expense_list(self, exp_list: list[list[str]]) -> None:
        pass

    @abstractmethod
    def register_cat_modifier(self, handler: Callable[[Category], None]):
        pass

    @abstractmethod
    def register_exp_modifier(self, handler: Callable[[Expense], None]):
        pass