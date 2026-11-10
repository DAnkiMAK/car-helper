"""Помощник по подбору авто — Streamlit-интерфейс."""
 
import streamlit as st
import pandas as pd

from core.data_loader import load_cars
from core.search import filter_cars
from core.sorting import sort_cars
from core.top_picks import top_picks
from core.market_benchmarks import market_benchmarks

st.set_page_config(page_title="Помощник по подбору авто", layout="wide")
st.title("🚗 Автоподборщик 🚗")


@st.cache_data
def get_data():
    """Загружает и чистит данные. Кэш: грузим один раз, а не при каждом действии."""
    return load_cars()



df = get_data()
# ===== Сайдбар: параметры поиска (функция №1) =====
st.sidebar.header("🔍 Фильтры поиска 🔍")

# Текстовые фильтры — выпадающие списки
make = st.sidebar.selectbox("Марка", [None] + sorted(df["make"].unique()))

# Модель показываем только если выбрана марка (иначе слишком много вариантов)
model = None
if make:
    models = sorted(df[df["make"] == make]["model"].unique())
    model = st.sidebar.selectbox("Модель", [None] + models)

fuel = st.sidebar.selectbox("Топливо", [None] + sorted(df["fuel"].unique()))
gear = st.sidebar.selectbox("Коробка передач", [None] + sorted(df["gear"].unique()))
offer_type = st.sidebar.selectbox("Состояние", [None] + sorted(df["offerType"].unique()))

# Числовые фильтры — диапазоны-слайдеры
price_range = st.sidebar.slider(
    "Цена, $",
    int(df["price"].min()), int(df["price"].max()),
    (int(df["price"].min()), int(df["price"].max())),
)
mileage_range = st.sidebar.slider(
    "Пробег, км",
    int(df["mileage"].min()), int(df["mileage"].max()),
    (int(df["mileage"].min()), int(df["mileage"].max())),
)
year_range = st.sidebar.slider(
    "Год выпуска",
    int(df["year"].min()), int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max())),
)
hp_range = st.sidebar.slider(
    "Мощность, л.с.",
    int(df["hp"].min()), int(df["hp"].max()),
    (int(df["hp"].min()), int(df["hp"].max())),
)

# ===== Сортировка (функция №2) =====
sort_by = st.sidebar.selectbox(
    "Сортировать по",
    ["price", "mileage", "year", "make", "model"],
    format_func=lambda x: {
        "price": "Цене", "mileage": "Пробегу", "year": "Году выпуска",
        "make": "Марке", "model": "Модели",
    }[x],
)
ascending = st.sidebar.checkbox("По возрастанию (от меньшего к большему)", value=True)

# ===== Применяем фильтры =====
result = filter_cars(
    df,
    make=make,
    model=model,
    fuel=fuel,
    gear=gear,
    offerType=offer_type,
    price_min=price_range[0],
    price_max=price_range[1],
    mileage_min=mileage_range[0],
    mileage_max=mileage_range[1],
    year_min=year_range[0],
    year_max=year_range[1],
    hp_min=hp_range[0],
    hp_max=hp_range[1],
)

result = sort_cars(result, by=sort_by, ascending=ascending)


st.subheader("Рыночные ориентиры")
if not make:
    st.info("Выберите марку в фильтрах, чтобы посмотреть ценовые ориентиры.")
else:
    # Берём всю таблицу: ограничение бюджета не должно менять ориентир цены.
    orientiry = market_benchmarks(df, make=make, model=model)
    if orientiry is None:
        st.info("Для выбранной марки и модели нет предложений.")
    else:
        group_name = f"{make} {model}" if model else make
        st.caption(
            f"Группа: {group_name}. Учитываются все объявления этой группы; "
            "остальные фильтры поиска на ориентиры не влияют. "
            "Типичный диапазон — от 25-го до 75-го процентиля, "
            "то есть середина распределения цен. Это цены объявлений из датасета."
        )
        kol, mediana, diapazon, granicy = st.columns(4)
        kol.metric("Количество предложений", orientiry["count"])
        mediana.metric("Медианная цена", f'{orientiry["median"]:,.2f}')
        diapazon.metric(
            "Типичный диапазон цен",
            f'{orientiry["q25"]:,.2f} – {orientiry["q75"]:,.2f}',
        )
        granicy.metric(
            "Минимум — максимум",
            f'{orientiry["min"]:,} – {orientiry["max"]:,}',
        )
        if not model:
            st.caption("Выберите также модель, чтобы сравнивать более узкую группу.")
        if orientiry["count"] < 5:
            st.caption("Предложений мало: ориентиры рассчитаны по небольшой выборке.")


st.subheader("Топ-5 предложений")
if result.empty:
    st.info("По заданным параметрам нет предложений.")
else:
    st.caption(
        "Среди найденных машин одинаково учитываются меньшая цена, "
        "меньший пробег и более свежий год выпуска."
    )
    st.dataframe(top_picks(result))

st.subheader(f"Найдено автомобилей: {len(result)} 🏎️")
st.dataframe(result)
