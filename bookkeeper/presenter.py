from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.view.view import View
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget


class Presenter:
    def __init__(self):
        self.cat_repo = SqliteRepository[Category]("data/client_category.db", Category)
        self.exp_repo = SqliteRepository[Expense]("data/client_expense.db", Expense)
        self.bud_repo = SqliteRepository[Budget]("data/client_budget.db", Budget)
        self.view = View(600, 800)
