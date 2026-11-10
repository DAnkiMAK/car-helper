"""Помощник по подбору авто — Streamlit-интерфейс."""
 
import streamlit as st
import pandas as pd

from core.data_loader import load_cars
from core.search import filter_cars
from core.sorting import sort_cars
from core.top_picks import top_picks
from core.price_fairness import assess_price_fairness

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


st.subheader("Топ-5 предложений")
if result.empty:
    st.info("По заданным параметрам нет предложений.")
else:
    st.caption(
        "Среди найденных машин одинаково учитываются меньшая цена, "
        "меньший пробег и более свежий год выпуска."
    )
    st.dataframe(top_picks(result))

# ===== Оценка справедливости цены (функция №3) =====
st.subheader("⚖️ Оценка справедливости цены")
st.caption(
    "Сравниваем цену авто с похожими предложениями: та же марка и модель, "
    "год выпуска ±1, пробег ±25%."
)

# Две колонки, чтобы поля ввода не растягивались на всю ширину.
# У каждого виджета свой key, чтобы не пересекаться с фильтрами в сайдбаре
col_left, col_right = st.columns(2)
with col_left:
    pf_make = st.selectbox("Марка оцениваемого авто", sorted(df["make"].unique()), key="pf_make")
    # Модели показываем только для выбранной марки
    pf_models = sorted(df[df["make"] == pf_make]["model"].unique())
    pf_model = st.selectbox("Модель оцениваемого авто", pf_models, key="pf_model")
    pf_year = st.number_input(
        "Год выпуска оцениваемого авто",
        min_value=int(df["year"].min()), max_value=int(df["year"].max()),
        value=int(df["year"].median()), step=1, key="pf_year",
    )
with col_right:
    pf_mileage = st.number_input(
        "Пробег оцениваемого авто, км",
        min_value=0, max_value=int(df["mileage"].max()),
        value=50000, step=1000, key="pf_mileage",
    )
    pf_price = st.number_input(
        "Цена оцениваемого авто, $",
        min_value=1, value=15000, step=500, key="pf_price",
    )

if st.button("Оценить цену", key="pf_button"):
    fairness = assess_price_fairness(df, pf_make, pf_model, pf_year, pf_mileage, pf_price)

    # Показываем вердикт разным цветом: красный - завышена, зеленый - выгодная
    if fairness["verdict"] == "завышена":
        st.error("Цена завышена по сравнению с рынком")
    elif fairness["verdict"] == "выгодная":
        st.success("Выгодное предложение: цена ниже рынка")
    elif fairness["verdict"] == "справедливая":
        st.info("Цена справедливая: близка к рыночной")
    else:
        st.warning(
            "Недостаточно данных: слишком мало похожих авто для оценки. "
            "Попробуйте другую модель или год выпуска."
        )

    # Подробности показываем, только если оценка получилась
    if fairness["market_median"] is not None:
        metric_1, metric_2, metric_3 = st.columns(3)
        metric_1.metric("Похожих авто найдено", fairness["similar_count"])
        metric_2.metric("Медианная цена похожих, $", f"{fairness['market_median']:.0f}")
        # delta_color="inverse": рост цены показывается красным (для покупателя это плохо)
        metric_3.metric(
            "Ваша цена относительно рынка",
            f"{pf_price}",
            delta=f"{fairness['difference_percent']:+.1f}%",
            delta_color="inverse",
        )

st.subheader(f"Найдено автомобилей: {len(result)} 🏎️")
st.dataframe(result)
