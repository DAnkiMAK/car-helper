import pandas as pd

from core.search import filter_cars
from core.top_picks import top_picks


def test_returns_five_best_and_preserves_input(cars_df):
    original = cars_df.copy()
    picks = top_picks(cars_df)

    assert len(picks) == 5
    assert picks["model"].tolist() == ["Corolla", "X1", "Golf", "Scenic", "Megane"]
    assert picks.columns.equals(cars_df.columns)
    pd.testing.assert_frame_equal(cars_df, original)


def test_respects_search_results(cars_df):
    matches = filter_cars(cars_df, make="Toyota")

    assert top_picks(matches)["model"].tolist() == ["Corolla", "Auris"]
    pd.testing.assert_frame_equal(top_picks(matches.iloc[:0]), matches.iloc[:0])


def test_prefers_lower_price_lower_mileage_and_newer_year():
    cars = pd.DataFrame(
        {
            "model": ["Дороже", "Больше пробег", "Старше", "Лучший вариант"],
            "price": [15000, 10000, 10000, 10000],
            "mileage": [50000, 100000, 50000, 50000],
            "year": [2020, 2020, 2010, 2020],
        }
    )

    assert top_picks(cars)["model"].tolist() == [
        "Лучший вариант", "Дороже", "Больше пробег", "Старше"
    ]


def test_equal_offers_keep_input_order(cars_df):
    cars = cars_df.assign(price=10000, mileage=50000, year=2020)

    pd.testing.assert_frame_equal(top_picks(cars), cars.head(5))
