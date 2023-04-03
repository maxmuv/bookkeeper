import datetime

from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.view.view import View
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget


class Presenter:
    def __init__(self) -> None:
        self.cat_repo = SqliteRepository[Category]("data/client_category.db", Category)
        self.exp_repo = SqliteRepository[Expense]("data/client_expense.db", Expense)
        self.bud_repo = SqliteRepository[Budget]("data/client_budget.db", Budget)
        self.view = View(600, 800)
        self.update_cat_view()
        self.update_exp_view()
        self.update_bdg_view()
        self.view.register_cat_adder(self.add_ctg)
        self.view.register_cat_remover(self.del_ctg)
        self.view.register_adder_handler(self.expense_adder_handler_for_ctg_view)
        self.view.register_exp_modifier(self.expense_modifier)
        self.view.register_budget_modifier(self.budget_modifier)
        # self.view.register_cat_modifier(self.ctg_modifier)
        self.view.register_exp_remover(self.del_handler)

    def update_cat_view(self) -> None:
        cats = self.cat_repo.get_all()
        list_cats = []
        if len(cats) != 0:
            for c in cats:
                if c.parent is not None:
                    list_cats.append((c.name,  self.cat_repo.get(c.parent).name))
                else:
                    list_cats.append((c.name, None))
        self.view.set_category_list(list_cats)

    def update_exp_view(self) -> None:
        exps = self.exp_repo.get_all()
        list_exps = []
        if len(exps) != 0:
            for e in exps:
                exp_cat = self.cat_repo.get(e.category)
                if exp_cat is None:
                    raise ValueError("Не существует категории для одного из расходов")
                list_exps.append([e.expense_date, str(e.amount), exp_cat.name, e.comment])
        self.view.set_expense_list(list_exps)
        self.update_bdg_view()

    def update_bdg_view(self) -> None:
        exps = self.exp_repo.get_all()
        budget_list = [[0, 0], [0, 0], [0, 0]]
        dt = datetime.datetime.now()
        if len(exps) != 0:
            for e in exps:
                exp_cat = self.cat_repo.get(e.category)
                if exp_cat is None:
                    raise ValueError("Не существует категории для одного из расходов")
                expdt = datetime.datetime.strptime(
                    str(e.expense_date), "%Y-%m-%d %H:%M:%S.%f")
                days_pass = abs((dt - expdt).days)
                if days_pass < 1:
                    budget_list[0][0] += e.amount
                if days_pass < 7:
                    budget_list[1][0] += e.amount
                th_month = (dt.month == expdt.month) and (dt.month == expdt.month)
                if th_month:
                    budget_list[2][0] += e.amount
        bdg_in_repo = self.bud_repo.get_all()
        for i, bdg in enumerate(bdg_in_repo):
            budget_list[i][1] = bdg.budget
        self.view.set_budget(budget_list)

    def del_ctg(self, name: str) -> None:
        cats = self.cat_repo.get_all({"name": name})
        if len(cats) != 0:
            if len(cats) > 1:
                raise ValueError("Категория должна иметь уникальное название")
            parents = self.cat_repo.get_all({"parent": cats[0].pk})
            if len(parents) != 0:
                raise ValueError("Можно удалить только лист дерева категорий")
            if len(self.exp_repo.get_all({"category": cats[0].pk})) != 0:
                raise ValueError("Нельзя удалить категорию, присутствующую в расходах")
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

    def expense_modifier(self, row: int, column: int, new_field: str) -> None:
        exps = self.exp_repo.get_all()
        exp = exps[row]
        if column == 0:
            exp.expense_date = datetime.datetime.strptime(
                new_field, "%Y-%m-%d %H:%M:%S.%f")
        elif column == 1:
            exp.amount = int(new_field)
        elif column == 2:
            cat = self.cat_repo.get_all({"name": new_field})
            if len(cat) == 0:
                raise ValueError("Не существует данной категории")
            exp.category = cat[0].pk
        elif column == 3:
            exp.comment = new_field
        self.exp_repo.update(exp)
        self.update_exp_view()

    def budget_modifier(self, row: int, column: int, new_field: str) -> None:
        bud_len = len(self.bud_repo.get_all())
        for i in range(bud_len, 3):
            bdg = Budget()
            self.bud_repo.add(bdg)
        bdg = Budget()
        bdg.pk = row
        bdg.budget = int(new_field)
        self.bud_repo.update(bdg)

    def ctg_modifier(self, prev: str, cur: str) -> None:
        if cur == "":
            ValueError("Название категории не может быть пустым")
        cat = self.cat_repo.get_all({"name": prev})[0]
        cat.name = cur
        self.cat_repo.update(cat)
        self.update_exp_view()
        self.update_cat_view()

    def del_handler(self, row: int) -> None:
        exps = self.exp_repo.get_all()
        for i in range(row, len(exps)):
            self.exp_repo.delete(exps[i].pk)
        for i in range(row + 1, len(exps)):
            self.exp_repo.add(exps[i])
        self.update_exp_view()
        self.update_bdg_view()
