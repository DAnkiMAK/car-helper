# Функция 4: Ценовые ориентиры для выбранной марки и модели

import pandas as pd

from core.search import filter_cars


def market_benchmarks(
    df: pd.DataFrame, make: str, model: str | None = None
) -> dict | None:
    # Для типичного диапазона берем границы 25% и 75%, между которыми находится средняя половина цен. Отбираем автомобили выбранной марки и, если указана, модели.
    otbor = filter_cars(df, make=make, model=model)
    if otbor.empty:
        return None

    # Рассчитываем ориентиры по ценам внутри этой группы.
    price = otbor["price"]
    result = {
        "count": len(otbor),
        "median": float(price.median()),
        "q25": float(price.quantile(0.25)),
        "q75": float(price.quantile(0.75)),
        "min": int(price.min()),
        "max": int(price.max()),
    }
    return result
