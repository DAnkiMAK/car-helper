"""Тесты для функции №1 - Быстрый поиск авто под потребности клиента """
from core.search import filter_cars


def test_filter_by_make(cars_df): #фильтр по марке
    """Поиск по марке возвращает только машины этой марки"""
    result = filter_cars(cars_df, make="BMW")
    assert len(result) == 3
    assert (result["make"] == "BMW").all()


def test_filter_by_budget(cars_df): #фильтр по потолку цены
    """Поиск по максимальной цене возвращает авто не дороже лимита"""
    result = filter_cars(cars_df, price_max=7000)
    assert len(result) > 0
    assert (result["price"] <= 7000).all()


def test_filter_price_range(cars_df): #фильтр по диапазону цены
    """Можно задать диапазон цены 'от и до'"""
    result = filter_cars(cars_df, price_min=7000, price_max=12000)
    assert (result["price"] >= 7000).all()
    assert (result["price"] <= 12000).all()


def test_filter_by_year_min(cars_df): #фильтр по году выпуска
    """Поиск по году: только авто не старше указанного"""
    result = filter_cars(cars_df, year_min=2015)
    assert (result["year"] >= 2015).all()


def test_filter_no_params_returns_all(cars_df): #без параметров вывод
    """Без параметров возвращается весь датафрейм"""
    assert len(filter_cars(cars_df)) == len(cars_df)


def test_filter_combined(cars_df): #комбинация параметров - марка, год выпуска, цена потолок
    """Комбинация параметров сужает выборку"""
    result = filter_cars(cars_df, make="BMW", price_max=13000, year_min=2013)
    assert len(result) == 1


def test_filter_does_not_modify_original(cars_df): #функция не изменяет ничего в данных
    """Функция не меняет исходный датафрейм"""
    before = len(cars_df)
    filter_cars(cars_df, make="BMW")
    assert len(cars_df) == before