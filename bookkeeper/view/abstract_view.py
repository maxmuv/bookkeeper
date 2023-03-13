from typing import Protocol, Callable
from abc import abstractmethod


class AbstractView(Protocol):
    @abstractmethod
    def set_category_list(self, cat_list: list[str]) -> None:
        pass

    @abstractmethod
    def set_budget(self, budget: list[list[int]]) -> None:
        pass

    @abstractmethod
    def set_expense_list(self, exp_list: list[list[str]]) -> None:
        pass

    @abstractmethod
    def register_cat_modifier(self, handler: Callable[[int], None]):
        pass

    @abstractmethod
    def register_exp_modifier(self, handler: Callable[[int, int, str], None]):
        pass

    def register_budget_modifier(self, handler: Callable[[int, int, str], None]):
        pass
