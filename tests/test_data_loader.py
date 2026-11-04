"""Тесты модуля загрузки данных"""

import pandas as pd

from core.data_loader import load_cars

def test_clean_cars_removes_empty_cells(cars_df):
    """В очищенном файле не должно быть пустых ячеек"""
    assert cars_df.notna().all().all()

def test_clean_cars_numeric_columns(cars_df):
    """Цена, пробег, мощность и год выпуска должны быть целыми числами"""
    for col in ("mileage", "price", "hp", "year"):
        assert cars_df[col].dtype.kind == "i" # "i" = integer


def test_load_cars_returns_dataframe():
    """load_cars возвращает Dataframe с данными"""
    df = load_cars()
    assert isinstance(df, pd.DataFrame) #эта таблица из пандаса?
    assert len(df) > 0 #в таблице есть хотя бы одна строка?
    assert {"make", "model", "price"}.issubset(df.columns) #есть такие колонки в таблице? (это базовый минимум для работы)


def test_load_cars_drops_empty_rows():
    """После загрузки нет пустых ячеек в колонках, в которых были пропуски (предварительный анализ через df.isna)"""
    df = load_cars()
    assert df["gear"].notna().all()
    assert df["model"].notna().all()
    assert df["hp"].notna().all()