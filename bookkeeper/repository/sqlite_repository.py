"""
Модуль описывает репозиторий, работающий с СУБД SQLite
"""
import datetime
import sqlite3
from inspect import get_annotations
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T

def convert_types(annotation_dict: dict)->list[str]:
    """
    Вспомогательная функция для перевода аннотации класса в строку типов для базы данных(для определение типа используются дефолтные объекты)

    Parameters
    ----------
    annotation_dict - аннотация класса

    Returns
    -------
    Список строк типов аттрибутов
    """
    res = []
    for t in list(annotation_dict.values()):
        if type(0) == t:
            res.append("integer")
        if type("") == t:
            res.append("text")
        if type(datetime.datetime.now()) == t:
            res.append("text")
    return res

def str2obj(cls: type, s: str)->T:
    args_tuple = s[0]
    res = cls(*args_tuple)
    return res

class SqliteRepository(AbstractRepository[T]):
    """
    Класс-репозиторий, который обеспечивает подключение к базе данных и работает с ней
    """
    def __init__(self, db_name: str, cls: type) -> None:
        """
        Подключает к базе данных, создает таблицу, если она не существует

        Parameters
        ----------
        db_name - название базы данных
        cls - тип хранимых объектов
        """
        self.db_name = db_name
        self.cls = cls
        self.fields = get_annotations(cls)
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        valuestype = convert_types(self.fields)
        creation_command = """CREATE TABLE IF NOT EXISTS t (\n"""
        for i, k in enumerate(self.fields):
            creation_command += f"{k} {valuestype[i]}"
            if k == "pk":
                creation_command += " PRIMARY KEY"
            if i+1 == len(self.fields):
                creation_command += ");"
            else:
                creation_command += ",\n"
        print(creation_command)
        self.cursor.execute(creation_command)
        self.connection.commit()

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        self.cursor.execute('PRAGMA foreign_keys = ON')
        self.cursor.execute(
            f'INSERT INTO t ({names}) VALUES ({p})', values
        )
        self.connection.commit()
        obj.pk = self.cursor.lastrowid
        return obj.pk

    def get(self, pk: int) -> T | None:
        get_command = f"SELECT * FROM t WHERE pk={pk}"
        self.cursor.execute(get_command)
        res_str = self.cursor.fetchall()
        return str2obj(self.cls, res_str)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        get_command = f"SELECT * FROM t"
        if bool(where):
            get_command += " WHERE "
            for i, k in enumerate(where):
                get_command += f"{k}={where[k]} "
                if i+1 != len(where):
                    get_command += "AND "
        self.cursor.execute(get_command)
        res_attrs = self.cursor.fetchall()
        res = []
        for attr in res_attrs:
            res.append(str2obj(attr))
        return res

    def update(self, obj: T) -> None:
        update_command = "UPDATE t SET "
        for i, k in enumerate(self.fields.keys()):
            if k != "pk":
                update_command += f"{k}={getattr(obj, k)}"
            if i+1 != len(self.fields.keys()):
                update_command += ", "
            update_command += f" WHERE pk = {getattr(obj, 'pk')}"
        self.cursor.execute(update_command)
        self.connection.commit()

    def delete(self, pk: int) -> None:
        removal_command = f"DELETE FROM t WHERE pk={pk}"
        self.cursor.execute(removal_command)
        self.connection.commit()

    def __del__(self) -> None:
        self.connection.close()

