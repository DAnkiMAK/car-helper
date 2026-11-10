"""Проверяем расчёт ценовых ориентиров на небольших наборах данных."""

import pandas as pd

from core.market_benchmarks import market_benchmarks


def test_benchmarks_by_make(cars_df):
    # У BMW три цены: 6800, 12500 и 16500.
    result = market_benchmarks(cars_df, make="BMW")

    assert result == {
        "count": 3,
        "median": 12500.0,
        "q25": 9650.0,
        "q75": 14500.0,
        "min": 6800,
        "max": 16500,
    }


def test_benchmarks_match_both_make_and_model(cars_df):
    # Одинаковое название модели у другой марки не должно попасть в расчёт.
    tab = cars_df.copy()
    tab.loc[tab["make"] == "Toyota", "model"] = "316"

    result = market_benchmarks(tab, make="BMW", model="316")

    assert result["count"] == 1
    assert result["median"] == 6800
    assert result["q25"] == result["q75"] == 6800
    assert result["min"] == result["max"] == 6800


def test_empty_selection_returns_none(cars_df):
    assert market_benchmarks(cars_df, make="Нет такой марки") is None
    assert market_benchmarks(cars_df, make="BMW", model="Golf") is None
    assert market_benchmarks(cars_df.iloc[:0], make="BMW") is None


def test_typical_range_with_expensive_offer(cars_df):
    # Проверяем границы на известных ценах, включая одно дорогое объявление.
    tab = cars_df.iloc[:5].copy()
    tab["make"] = "BMW"
    tab["model"] = "320"
    tab["price"] = [10000, 11000, 12000, 13000, 100000]

    result = market_benchmarks(tab, make="BMW", model="320")

    assert result["count"] == 5
    assert result["median"] == 12000
    assert result["q25"] == 11000
    assert result["q75"] == 13000
    assert result["min"] == 10000
    assert result["max"] == 100000


def test_even_number_of_offers(cars_df):
    result = market_benchmarks(cars_df, make="Volkswagen")

    assert result["count"] == 2
    assert result["median"] == 8338.5
    assert result["q25"] == 7607.75
    assert result["q75"] == 9069.25


def test_equal_prices(cars_df):
    tab = cars_df.assign(price=10000)

    result = market_benchmarks(tab, make="BMW")

    assert result["count"] == 3
    assert result["median"] == 10000
    assert result["q25"] == result["q75"] == 10000
    assert result["min"] == result["max"] == 10000


def test_does_not_modify_original(cars_df):
    before = cars_df.copy(deep=True)

    market_benchmarks(cars_df, make="BMW", model="320")

    pd.testing.assert_frame_equal(cars_df, before)
