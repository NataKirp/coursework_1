import json
from collections import defaultdict
from datetime import datetime
from typing import Any, Hashable

from pandas import DataFrame

from src.logging_config import setup_logging

services_logger = setup_logging("services")


def df_to_dict(df: DataFrame) -> list[dict[Hashable, Any]]:
    """Функция для преобразования датафрейма в список словарей."""
    services_logger.info('Начало работы функции "df_to_dict".')
    if df is None or df.empty:
        services_logger.warning("💥 В датафрейме нет данных.")
        return []

    data_list = df.to_dict(orient="records")
    services_logger.info('✅ Завершение работы функции "df_to_dict".')

    return data_list


def cashback_analysis(data: list[dict], year: int, month: int):
    """Функция для анализа выгодности категорий повышенного кэшбэка."""
    services_logger.info('Начало работы функции "cashback_analysis".')
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        services_logger.error(
            "❌ Ошибка типа данных: data должна быть списком словарей."
        )
        raise TypeError(
            "❌ Неправильный формат исходных данных. Ожидается список словарей"
        )
    if not isinstance(year, int) or not isinstance(month, int):
        services_logger.error(
            f"❌ Неверные параметры периода: year={type(year)}, month={type(month)}"
        )
        raise ValueError("Год или месяц для расчета отсутствует или имеет неверный тип")
    if not data:
        services_logger.warning("💥 Список транзакций пуст")
        return []

    filtered_by_month_year = [
        item
        for item in data
        if (d := datetime.strptime(item["Дата операции"], "%d.%m.%Y %H:%M:%S")).month
        == month
        and d.year == year
    ]

    filtered_by_category: defaultdict[str, int] = defaultdict(int)
    for item in filtered_by_month_year:
        filtered_by_category[item["Категория"]] += item["Кэшбэк"]

    sorted_by_category = dict(
        sorted(filtered_by_category.items(), key=lambda x: x[1], reverse=True)
    )
    # округляем значения кэшбэка и исключаем значения, где кэшбэк 0
    sorted_by_category = {
        k: round(v) for k, v in sorted_by_category.items() if round(v) != 0
    }

    if not sorted_by_category:
        services_logger.info("💥 За указанный период кэшбэк не найден.")
        return json.dumps(
            {"message": f"За {month}.{year} кэшбэка нет"}, ensure_ascii=False
        )

    json_output = json.dumps(sorted_by_category, indent=4, ensure_ascii=False)
    services_logger.info('✅ Завершение работы функции "cashback_analysis".')

    return json_output
