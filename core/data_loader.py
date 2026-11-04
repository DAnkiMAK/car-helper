"""Загрузим и подготовим данные об автомобилях из датасета csv"""

from pathlib import Path

import pandas as pd

"""Данные лежат в папке проекта: car-helper/data"""
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFOULT_CSV = DATA_DIR / "cars_germany.csv"


def clean_cars(df: pd.DataFrame) -> pd.DataFrame:
    """Убираем пустые ячейки и приводим числовые колонки к целому типу"""
    df = df.copy()
    df = df.dropna()
    for col in ("mileage", "price", "hp", "year"):
        df[col] = df[col].astype(int) #приводим колонки в числовой тип
    return df


def load_cars(path=DEFOULT_CSV) -> pd.DataFrame:
    """Загружаем датасет из csv и преобразуем его в очищенный датафрейм"""
    df = pd.read_csv(path)
    return clean_cars(df)