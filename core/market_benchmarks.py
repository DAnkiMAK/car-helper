"""Функция №4: ценовые ориентиры для выбранной марки и модели."""

import pandas as pd

from core.search import filter_cars


def market_benchmarks(
    df: pd.DataFrame, make: str, model: str | None = None
) -> dict | None:
    """Возвращаем число предложений, медиану и границы цен выбранной группы.

    Типичный диапазон задаём квартилями 25% и 75%: середина распределения
    меньше зависит от отдельных дорогих или дешёвых объявлений.
    Передаём очищенную таблицу до применения бюджетных и других фильтров.
    Если предложений нет, возвращаем None.
    """
    # Отбираем автомобили выбранной марки и, если указана, модели.
    otbor = filter_cars(df, make=make, model=model)
    if otbor.empty:
        return None

    # Рассчитываем ориентиры по ценам внутри этой группы.
    ceny = otbor["price"]
    result = {
        "count": len(otbor),
        "median": float(ceny.median()),
        "q25": float(ceny.quantile(0.25)),
        "q75": float(ceny.quantile(0.75)),
        "min": int(ceny.min()),
        "max": int(ceny.max()),
    }
    return result
