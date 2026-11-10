"""Функция 3: оценка справедливости цены автомобиля.

Идея: находим на рынке похожие авто (та же марка, модель, близкий год
и близкий пробег) и сравниваем цену нашего авто с медианной ценой похожих.
"""
import pandas as pd

# Настройки по умолчанию - их можно менять при вызове функций
YEAR_TOLERANCE = 1          # допустимая разница в годах выпуска (+/- 1 год)
MILEAGE_TOLERANCE = 0.25    # допустимая разница в пробеге (+/- 25%)
MIN_MILEAGE_RANGE = 5000    # минимальный запас по пробегу в км (нужен для авто с пробегом около 0)
MIN_SIMILAR_CARS = 5        # меньше похожих авто - данных недостаточно для вывода
FAIR_RANGE_PERCENT = 10     # отклонение от медианы до +/- 10% считаем справедливой ценой


def find_similar_cars(df, make, model, year, mileage,
                      year_tolerance=YEAR_TOLERANCE,
                      mileage_tolerance=MILEAGE_TOLERANCE):
    """Возвращает таблицу авто, похожих на заданное.

    Похожее авто: та же марка и модель, год выпуска в пределах
    year_tolerance, пробег в пределах mileage_tolerance от заданного.
    """
    # Допустимый разброс пробега: процент от пробега, но не меньше MIN_MILEAGE_RANGE
    mileage_range = max(mileage * mileage_tolerance, MIN_MILEAGE_RANGE)

    # Булева маска: все условия объединяем через & ("и")
    mask = (
        (df['make'] == make)
        & (df['model'] == model)
        & (df['year'].between(year - year_tolerance, year + year_tolerance))
        & (df['mileage'].between(mileage - mileage_range, mileage + mileage_range))
    )
    return df[mask]


def assess_price_fairness(df, make, model, year, mileage, price,
                          min_similar=MIN_SIMILAR_CARS,
                          fair_range_percent=FAIR_RANGE_PERCENT):
    """Оценивает, насколько цена авто соответствует рынку.

    Возвращает словарь:
      verdict            - 'завышена', 'справедливая', 'выгодная' или 'недостаточно данных'
      similar_count      - сколько похожих авто нашлось
      market_median      - медианная цена похожих авто (или None)
      difference_percent - на сколько % цена выше (+) или ниже (-) медианы (или None)
    """
    # Защита от некорректного ввода
    if price <= 0:
        raise ValueError('Цена должна быть больше нуля')

    similar = find_similar_cars(df, make, model, year, mileage)
    similar_count = len(similar)

    # Если похожих авто слишком мало, вывод был бы ненадежным
    if similar_count < min_similar:
        return {
            'verdict': 'недостаточно данных',
            'similar_count': similar_count,
            'market_median': None,
            'difference_percent': None,
        }

    # Медиана устойчива к редким слишком дорогим или слишком дешевым объявлениям
    market_median = float(similar['price'].median())
    difference_percent = (price - market_median) / market_median * 100

    if difference_percent > fair_range_percent:
        verdict = 'завышена'
    elif difference_percent < -fair_range_percent:
        verdict = 'выгодная'
    else:
        verdict = 'справедливая'

    return {
        'verdict': verdict,
        'similar_count': similar_count,
        'market_median': market_median,
        'difference_percent': round(difference_percent, 1),
    }
