from dataclasses import dataclass, field
import datetime

from bookkeeper.repository.sqlite_repository import SqliteRepository
import pytest

@pytest.fixture
def simple_class():
    class Simple():
        """Класс с аттрибутом pk"""
        pk: int

    return Simple

@pytest.fixture
def fewattr_class():
    @dataclass(slots=True)
    class FewAttr():
        """Класс с несколькими аттрибутами"""
        pk: int = 0
        s: str = "some string"
        t: datetime = field(default_factory=datetime.datetime.now)
        i: int = 0

        def __eq__(self, other):
            if not isinstance(other, FewAttr):
                return NotImplemented

            return self.pk == other.pk and self.s == other.s \
                and str(self.t) == str(other.t) and self.i == other.i

    return FewAttr

@pytest.fixture
def repo_simple(simple_class):
    return SqliteRepository('test_simple.db', simple_class, True)

@pytest.fixture
def repo_few(fewattr_class):
    return SqliteRepository('test_few.db', fewattr_class, True)

def test_crud_simple(simple_class, repo_simple):
    obj1 = simple_class()
    obj1.pk = 0
    pk = repo_simple.add(obj1)
    assert repo_simple.get(obj1.pk).pk == obj1.pk
    assert pk == obj1.pk
    obj2 = simple_class()
    obj2.pk = pk
    repo_simple.update(obj2)
    assert repo_simple.get(pk).pk == pk
    repo_simple.delete(pk)
    assert repo_simple.get(pk) is None

def test_crud_few(fewattr_class, repo_few):
    obj1 = fewattr_class()
    pk = repo_few.add(obj1)
    assert repo_few.get(obj1.pk) == obj1
    assert pk == obj1.pk
    obj2 = fewattr_class()
    obj2.pk = pk
    repo_few.update(obj2)
    assert repo_few.get(pk) == obj2
    repo_few.delete(pk)
    assert repo_few.get(pk) is None