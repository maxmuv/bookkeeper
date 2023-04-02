from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.view.view import View
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget


class Presenter:
    def __init__(self):
        self.cat_repo = SqliteRepository[Category]("data/client_category.db", Category, True)
        self.exp_repo = SqliteRepository[Expense]("data/client_expense.db", Expense, True)
        self.bud_repo = SqliteRepository[Budget]("data/client_budget.db", Budget, True)
        self.view = View(600, 800)
        self.update_cat_view()
        self.update_exp_view()
        self.view.register_cat_adder(self.add_ctg)
        self.view.register_cat_remover(self.del_ctg)
        self.view.register_adder_handler(self.expense_adder_handler_for_ctg_view)

    def update_cat_view(self):
        cats = self.cat_repo.get_all()
        list_cats = []
        if len(cats) != 0:
            for c in cats:
                if c.parent is not None:
                    list_cats.append((c.name,  self.cat_repo.get(c.parent).name))
                else:
                    list_cats.append((c.name, None))
        self.view.set_category_list(list_cats)

    def update_exp_view(self):
        exps = self.exp_repo.get_all()
        list_exps = []
        if len(exps) != 0:
            for e in exps:
                exp_cat = self.cat_repo.get(e.category)
                if exp_cat is None:
                    raise ValueError("Не существует категории для одного из расходов")
                list_exps.append([e.expense_date, str(e.amount), exp_cat.name])
        self.view.set_expense_list(list_exps)

    def del_ctg(self, name: str) -> None:
        cats = self.cat_repo.get_all({"name": name})
        if len(cats) != 0:
            if len(cats) > 1:
                raise ValueError("Категория должна иметь уникальное название")
            parents = self.cat_repo.get_all({"parent": cats[0].pk})
            if len(parents) != 0:
                raise ValueError("Можно удалить только лист дерева категорий")
            self.cat_repo.delete(cats[0].pk)
        self.update_cat_view()

    def add_ctg(self, parent_name: str | None, name: str) -> None:
        if name == "":
            raise ValueError("Имя категории не должно быть пустым")
        if len(self.cat_repo.get_all({"name": name})) != 0:
            raise ValueError("Имя категории должно быть уникальным")
        parent_ids = self.cat_repo.get_all({"name": parent_name})
        cat = Category()
        if len(parent_ids) != 0:
            cat.parent = parent_ids[-1].pk
        cat.name = name
        self.cat_repo.add(cat)
        self.update_cat_view()

    def expense_adder_handler_for_ctg_view(self, amount: int, ctg_name: str) -> None:
        req_ctg = self.cat_repo.get_all({"name": ctg_name})
        if len(req_ctg) != 1:
            raise ValueError("Нет подходящей категории")
        exp = Expense()
        exp.amount = amount
        exp.category = req_ctg[0].pk
        self.exp_repo.add(exp)
        self.update_exp_view()
