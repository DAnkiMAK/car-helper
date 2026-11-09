# 📋 Как подключиться к проекту car-helper

## Шаг 1. Принять приглашение

Тебе на почту GitHub пришло приглашение стать collaborator — прими его (ссылка в письме или в уведомлениях GitHub → Inbox).

## Шаг 2. Склонировать репозиторий

```bash
git clone https://github.com/DAnkiMAK/car-helper.git
cd car-helper
```

## Шаг 3. Настроить окружение

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Шаг 4. Проверить, что всё работает

```bash
pytest
```

Должно быть **`18 passed`**. Если так — база в порядке, можно браться за свою часть.

---

# 🎯 Какая часть твоя

| Твоя функция | Что делаешь | Файлы |
|---|---|---|
| **№3 — Справедливость цены** | Подсказывает, не завышена ли цена авто по сравнению с похожими (той же марки, модели, года, близкого пробега) | `core/price_fairness.py`, `tests/test_price_fairness.py` |
| **№4 — Рыночные ориентиры** | Показывает типичный ценовой диапазон для марки/модели | `core/market_benchmarks.py`, `tests/test_market_benchmarks.py` |
| **№5 — Топ-5 предложений** | Выдаёт 5 лучших вариантов под запрос покупателя | `core/top_picks.py`, `tests/test_top_picks.py` |

Уточни у тимлида, какая за тобой закреплена.

---

# 🛠 Как реализовать функцию

1. **Создай свою ветку** (имя — по номеру функции):

   ```bash
   git checkout -b feature/price-fairness
   ```

2. **Создай файл функции** `core/<имя>.py`. Пиши **чистые функции**, которые принимают `DataFrame` и возвращают `DataFrame`/значение. Данные уже загружены и почищены — не грузи их заново:

   ```python
   import pandas as pd
   from core.data_loader import load_cars
   ```

3. **Создай тест** `tests/test_<имя>.py`. Используй фикстуру `cars_df` из `tests/conftest.py` — маленький образец данных, не грузи весь датасет:

   ```python
   def test_что_проверяем(cars_df):
       result = твоя_функция(cars_df)
       assert ...
   ```

4. **Подключи результат в `app.py`**, если это нужно интерфейсу (посмотри, как подключены функции 1 и 2).

**Правило:** все тесты должны проходить — **и старые, и твои новые**:

```bash
pytest
```

---

# 🔀 Как слить свою часть

**Прямо в `main` пушить НЕЛЬЗЯ** — ветка защищена, GitHub отклонит. Только через Pull Request:

```bash
git add .
git commit -m "Добавлена функция 3: справедливость цены"
git push -u origin feature/price-fairness
```

Потом на GitHub открой **Pull Requests → New pull request** (твоя ветка → `main`) и жди, пока тимлид проверит и сольёт.

**Перед каждым началом работы** подтяни свежие изменения:

```bash
git pull origin main
```

---

# ⚡ Коротко для тех, кто уже в курсе git

```
clone → venv → pip install -r requirements.txt → pytest (18 passed)
→ git checkout -b feature/твоя_функция
→ пиши core/твоя.py + tests/test_твоя.py (фикстура cars_df из conftest)
→ pytest (все зелёные) → push своей ветки → Pull Request в main
```