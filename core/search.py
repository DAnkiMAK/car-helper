"""Функция №1 - Быстрый поиск авто под потребности клиента """

import pandas as pd

def filter_cars(df: pd.DataFrame,
                make: str | None = None,
                model: str | None = None,
                fuel: str | None = None,
                gear: str | None = None,
                offerType: str | None = None,
                price_min: int | None = None,
                price_max: int | None = None,
                mileage_min: int | None = None,
                mileage_max: int | None = None,
                hp_min: int | None = None,
                hp_max: int | None = None,
                year_min: int | None = None,
                year_max: int | None = None) -> pd.DataFrame:
    
    """Фильтруем датафрейм по заданным параметрам"""
    result = df.copy()
    #Для текстовых параметров - точное совпадение используем:
    if make:
        result = result[result["make"] == make]
    if model:
        result = result[result["model"] == model]
    if fuel:
        result = result[result["fuel"] == fuel]
    if gear:
        result = result[result["gear"] == gear]
    if offerType:
        result = result[result["offerType"] == offerType]

    #Для числовых параметров - диапазон границ используем:
    if price_min is not None:
        result = result[result["price"] >= price_min]
    if price_max is not None:
        result = result[result["price"] <= price_max]
    if mileage_min is not None:
        result = result[result["mileage"] >= mileage_min]
    if mileage_max is not None:
        result = result[result["mileage"] <= mileage_max]
    if hp_min is not None:
        result = result[result["hp"] >= hp_min]
    if hp_max is not None:
        result = result[result["hp"] <= hp_max]
    if year_min is not None:
        result = result[result["year"] >= year_min]
    if year_max is not None:
        result = result[result["year"] <= year_max]

    return result