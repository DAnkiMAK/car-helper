"""Тесты для функции №3 - Справедливость цены"""

import pandas as pd
import pytest

from core.price_fairness import find_similar_cars, assess_price_fairness


@pytest.fixture
def market_df():
    """Небольшой образец рынка: 7 похожих Golf и несколько "неподходящих" авто.
    Своя фикстура нужна, потому что в cars_df слишком мало одинаковых моделей для сравнения цен."""
    rows = [
        # (make, model, year, mileage, price) - похожие Golf, медиана цены = 20000
        ("Volkswagen", "Golf", 2018, 50000, 19000),
        ("Volkswagen", "Golf", 2018, 52000, 19500),
        ("Volkswagen", "Golf", 2019, 48000, 20000),
        ("Volkswagen", "Golf", 2018, 55000, 20000),
        ("Volkswagen", "Golf", 2019, 45000, 20500),
        ("Volkswagen", "Golf", 2017, 56000, 21000),
        ("Volkswagen", "Golf", 2018, 51000, 21500),
        # Не подходят: другой год, другой пробег, другая модель, другая марка
        ("Volkswagen", "Golf", 2013, 50000, 9000),
        ("Volkswagen", "Golf", 2018, 150000, 12000),
        ("Volkswagen", "Polo", 2018, 50000, 14000),
        ("Audi", "A3", 2018, 50000, 25000),
    ]
    return pd.DataFrame(rows, columns=["make", "model", "year", "mileage", "price"])


def test_find_similar_cars_keeps_only_matching(market_df):
    """В результат попадают только Golf нужного года и пробега"""
    similar = find_similar_cars(market_df, "Volkswagen", "Golf", 2018, 50000)
    assert len(similar) == 7  # проверяем, что "неподходящие" авто отброшены
    assert set(similar["model"]) == {"Golf"}
    assert similar["year"].between(2017, 2019).all()


def test_find_similar_cars_unknown_model_returns_empty(market_df):
    """Если такой модели нет в таблице, результат пустой"""
    similar = find_similar_cars(market_df, "Volkswagen", "Phaeton", 2018, 50000)
    assert similar.empty


def test_overpriced_car(market_df):
    """Цена на 25% выше медианы - вердикт "завышена" """
    result = assess_price_fairness(market_df, "Volkswagen", "Golf", 2018, 50000, 25000)
    assert result["verdict"] == "завышена"
    assert result["market_median"] == 20000
    assert result["difference_percent"] == 25.0


def test_fair_price(market_df):
    """Цена близка к медиане - вердикт "справедливая" """
    result = assess_price_fairness(market_df, "Volkswagen", "Golf", 2018, 50000, 20500)
    assert result["verdict"] == "справедливая"
    assert result["similar_count"] == 7


def test_good_deal(market_df):
    """Цена на 20% ниже медианы - вердикт "выгодная" """
    result = assess_price_fairness(market_df, "Volkswagen", "Golf", 2018, 50000, 16000)
    assert result["verdict"] == "выгодная"
    assert result["difference_percent"] == -20.0


def test_not_enough_similar_cars(market_df):
    """Для Audi A3 в выборке всего одно похожее авто - данных недостаточно"""
    result = assess_price_fairness(market_df, "Audi", "A3", 2018, 50000, 25000)
    assert result["verdict"] == "недостаточно данных"
    assert result["similar_count"] == 1
    assert result["market_median"] is None


def test_zero_mileage_does_not_break(market_df):
    """Новое авто с нулевым пробегом: функция не падает"""
    result = assess_price_fairness(market_df, "Volkswagen", "Golf", 2019, 0, 30000)
    assert result["verdict"] == "недостаточно данных"


@pytest.mark.parametrize("bad_price", [0, -100])
def test_invalid_price_raises_error(market_df, bad_price):
    """Нулевая или отрицательная цена вызывает ошибку"""
    with pytest.raises(ValueError):
        assess_price_fairness(market_df, "Volkswagen", "Golf", 2018, 50000, bad_price)


def test_shared_fixture_not_enough_data(cars_df):
    """На общем образце cars_df похожих авто мало - данных недостаточно"""
    result = assess_price_fairness(cars_df, "BMW", "316", 2011, 235000, 6800)
    assert result["verdict"] == "недостаточно данных"
    assert result["similar_count"] == 1  # нашлось только само это авто


def test_shared_fixture_with_min_similar_one(cars_df):
    """Если снизить порог до 1, оценка считается даже по одному авто"""
    result = assess_price_fairness(cars_df, "BMW", "316", 2011, 235000, 6800, min_similar=1)
    assert result["verdict"] == "справедливая"
    assert result["market_median"] == 6800


def test_assess_does_not_modify_original(cars_df):
    """Оценка цены не меняет исходный датафрейм"""
    before = cars_df.copy()
    assess_price_fairness(cars_df, "BMW", "316", 2011, 235000, 6800, min_similar=1)
    assert cars_df.equals(before)  # проверяем, что таблица осталась прежней
