import pytest
from hashmap import SpecialHashMap


def test_iloc():
    map = SpecialHashMap()
    map["value1"] = 1
    map["value2"] = 2
    map["value3"] = 3
    map["1"] = 10
    map["2"] = 20
    map["3"] = 30
    map["1, 5"] = 100
    map["5, 5"] = 200
    map["10, 5"] = 300

    # Проверяем значения по индексам
    assert map.iloc[0] == 10  # Проверка первого элемента
    assert map.iloc[2] == 300  # Проверка третьего элемента
    assert map.iloc[5] == 200  # Проверка шестого элемента
    assert map.iloc[8] == 3  # Проверка девятого элемента


def test_ploc_single_condition():
    map = SpecialHashMap()
    map["value1"] = 1
    map["value2"] = 2
    map["value3"] = 3
    map["1"] = 10
    map["2"] = 20
    map["3"] = 30
    map["(1, 5)"] = 100
    map["(5, 5)"] = 200
    map["(10, 5)"] = 300
    map["(1, 5, 3)"] = 400
    map["(5, 5, 4)"] = 500
    map["(10, 5, 5)"] = 600

    # Проверяем фильтрацию по одному условию
    assert map.ploc[">=1"] == {"1": 10, "2": 20, "3": 30}
    assert map.ploc["<3"] == {"1": 10, "2": 20}


def test_ploc_multiple_conditions():
    map = SpecialHashMap()
    map["(1, 5)"] = 100
    map["(5, 5)"] = 200
    map["(10, 5)"] = 300
    map["(1, 5, 3)"] = 400
    map["(5, 5, 4)"] = 500
    map["(10, 5, 5)"] = 600

    # Проверяем фильтрацию по нескольким условиям
    assert map.ploc[">0, >0"] == {"(1, 5)": 100, "(5, 5)": 200, "(10, 5)": 300}
    assert map.ploc[">=10, >0"] == {"(10, 5)": 300}
    assert map.ploc["<5, >=5, >=3"] == {"(1, 5, 3)": 400}
    assert map.ploc["<5, >=5, >=3, >4"]=={}

def test_ploc_exceptions():
    map = SpecialHashMap()

    # Проверяем исключения для неверного формата условия
    with pytest.raises(ValueError, match="Invalid condition format"):
        map.ploc[">a"]

    # Проверяем исключение для выхода за пределы индекса
    with pytest.raises(IndexError, match="Index out of range"):
        _ = map.iloc[100]
