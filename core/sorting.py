"""Функция №2 - сравнение и сортировка предложений
Пользователь может сортировать показ авто по цене, пробегу и году выпуска, чтобы первыми были предложения максимально подходящие для него"""

import pandas as pd

sort_columns = ("price", "mileage", "year", "make", "model") #список колонок, по которым можно сортировать

def sort_cars(df: pd.DataFrame, 
              by: str = "price", 
              ascending: bool = True) -> pd.DataFrame:
    """Сортируем датафрейм по заданным параметрам:
    by         - поле для сортировки: 'price', 'mileage', 'year', "make", "model".
    ascending  - True = по возрастанию (от меньшего к большему),
                 False = по убыванию (от большего к меньшему).
    """
    if by not in sort_columns:
        raise ValueError(f"Поле {by} нельзя использовать для сортировки. Допустимые значения для сортировки: {sort_columns}")
    return df.sort_values(by=by, ascending=ascending)