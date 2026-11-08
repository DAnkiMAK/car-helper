"""Функция №5: пять лучших предложений среди результатов поиска."""

import pandas as pd


def top_picks(df: pd.DataFrame) -> pd.DataFrame:
    """Учитывает цену, пробег и год выпуска с одинаковым весом.

    Оценки сравниваются внутри текущей выборки. При равенстве баллов
    сохраняется порядок входной таблицы.
    """
    if df.empty:
        return df.copy()

    score = pd.Series(0.0, index=df.index)
    for column in ("price", "mileage", "year"):
        values = df[column]
        low = values.min()
        high = values.max()

        # Одинаковое значение у всех машин не влияет на порядок.
        if high == low:
            continue

        if column == "year":
            score += (values - low) / (high - low)
        else:
            score += (high - values) / (high - low)

    order = (-score).to_numpy().argsort(kind="stable")
    return df.iloc[order[:5]].copy()
