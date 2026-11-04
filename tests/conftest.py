"""Фиксируем небольшой объем данных по машинам для тестов"""

import pandas as pd
import pytest

from core.data_loader import clean_cars

@pytest.fixture
def cars_df():
    """Небольшой очищенный датафрейм для быстрых тестов (чтобы не брать весь датафрейм)"""
    data = {
         "mileage": [235000, 120000, 90000, 92800, 150000, 147000, 85000, 96200, 91894],
              "make": ["BMW", "BMW", "BMW", "Volkswagen", "Volkswagen", "Toyota", "Toyota", "Renault", "Renault"],
              "model": ["316", "320", "X1", "Golf", "Passat", "Auris", "Corolla", "Megane", "Scenic"],
              "fuel": ["Diesel", "Gasoline", "Diesel", "Gasoline", "Diesel", "Electric/Gasoline", "Gasoline", "Gasoline", "Diesel"],
              "gear": ["Manual", "Automatic", "Automatic", "Manual", "Automatic", "Automatic", "Manual", "Manual", "Manual"],
              "offerType": ["Used", "Used", "Used", "Used", "Used", "Used", "Used", "Used", "Used"],
           "price": [6800, 12500, 16500, 6877, 9800, 6950, 11500, 6950, 6970],
         "hp": [116, 184, 150, 122, 150, 99, 132, 110, 131],
         "year": [2011, 2015, 2018, 2011, 2013, 2011, 2016, 2011, 2011],
        }
    return clean_cars(pd.DataFrame(data))
    