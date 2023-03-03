"""
Модуль описывает репозиторий, работающий с СУБД SQLite
"""

import sqlite3
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SqliteRepository(AbstractRepository[T]):
    def __init__(self) -> None:
        pass

    def add(self, obj: T) -> int:
        pass

    def get(self, pk: int) -> T | None:
        pass

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        pass

    def update(self, obj: T) -> None:
        pass

    def delete(self, pk: int) -> None:
        pass

    def __del__(self) -> None:
        pass