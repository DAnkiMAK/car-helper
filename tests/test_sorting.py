"""Тесты для функции №2 - Сравнение и сортировка предложений"""

import pytest

from core.sorting import sort_cars

def test_sort_by_price_ascending(cars_df):    
    """По умолчанию (если параметр не задан) сортирует по цене по возрастанию"""
    result = sort_cars(cars_df)
    assert result["price"].is_monotonic_increasing #проверяем, что цена идёт по возрастанию монотонно


def test_sort_by_price_descending(cars_df):
    """ascending=False сортирует по цене по убыванию - противоположно тесту раннее"""
    result = sort_cars(cars_df, by="price", ascending=False)
    assert result["price"].is_monotonic_decreasing #проверяем, что цена идёт по убыванию монотонно


def test_sort_by_year(cars_df):
    """Сортировка по году выпуска по возрастанию"""
    result = sort_cars(cars_df, by="year")
    assert result["year"].is_monotonic_increasing #проверяем, что год идёт по возрастанию монотонно


def test_sort_by_make(cars_df):
    """Сортировка по марке идёт по алфавиту"""
    result = sort_cars(cars_df, by="make")
    assert list(result["make"]) == sorted(list(result["make"])) #превращаем в список марок и его проверяем на алфавитный порядок


def test_sort_by_mileage(cars_df):
    """Сортировка по пробегу по возрастанию"""
    result = sort_cars(cars_df, by="mileage")
    assert result["mileage"].is_monotonic_increasing #проверяем, что пробег идёт по возрастанию монотонно


def test_invalid_field(cars_df):
    """Неразрешённое поле вызывает ошибку"""
    with pytest.raises(ValueError):
        sort_cars(cars_df, by="fuel") #проверяем, что ошибка вызывается при попытке сортировки по типу топлива


def test_sort_does_not_modify_original(cars_df):
    """Сортировка не меняет исходный датафрейм"""
    before = list(cars_df["price"])
    sort_cars(cars_df, by="price")
    assert list(cars_df["price"]) == before #проверяем, что исходный датафрейм не изменился

