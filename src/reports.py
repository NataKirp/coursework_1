import json
import datetime
from functools import wraps
from pathlib import Path
from typing import Optional, List, Any, Callable

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.logging_config import setup_logging
from src.utils import read_excel_file

reports_logger = setup_logging('reports')


def save_report(filename: str = 'report'):
    """
    Декоратор для сохранения результатов выполнения функций-отчетов.
    Если не задан `filename`, записывается в файл с именем по умолчанию.
    """

    def wrapper(func: Callable[..., Any]):
        """Возвращает обёртку, которая сохраняет результат выполнение функции `func`."""

        @wraps(func)
        def inner(*args: Any, **kwargs: Any):
            """Обёртка для выполнения функции `func`."""
            root_dir = Path(__file__).resolve().parent.parent
            reports_dir = root_dir / 'reports'
            reports_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.datetime.now().strftime('%Y%m%d')
            filename_date = f'{filename}_{timestamp}.json'

            full_path = reports_dir / filename_date
            reports_logger.info(f'Начало работы функции "{func.__name__}".')
            result = func(*args, **kwargs)

            with open(full_path, 'w', encoding="utf-8") as file:
                file.write(result)

            reports_logger.info(f'Завершение работы функции "{func.__name__}".')
            reports_logger.info(f'Данные сохранены в: {full_path}')

            return result

        return inner

    return wrapper


@save_report()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> list[Any] | str:
    """Функция для вычисления трат по заданной категории за последние три месяца (от переданной даты)."""
    if date is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    start_date = end_date - relativedelta(months=3)

    reports_logger.info(f'Период для анализа данных: с {start_date} по {end_date}.')
    filtered_by_date = transactions[
        (transactions['Дата операции'] >= start_date) & (transactions['Дата операции'] <= end_date)]

    if filtered_by_date is None or filtered_by_date.empty:
        reports_logger.info('Нет данных за указанный период')
        return []

    filtered_by_category = filtered_by_date[filtered_by_date['Категория'] == category]
    reports_logger.info(f'Выбрана категория {category}')

    if filtered_by_category is None or filtered_by_category.empty:
        reports_logger.info('Нет данных за указанный период')
        return []

    grouped = filtered_by_category.groupby('Описание')['Сумма операции'].sum().reset_index()
    grouped = grouped.sort_values(by='Сумма операции', ascending=True)  # True, т.к. суммы отрицательные, по убыванию
    # создаем словарь под каждое описание
    output_list = grouped.to_dict(orient='records')
    output = {category: output_list}
    json_output = json.dumps(output, indent=4, ensure_ascii=False)

    return json_output


if __name__ == '__main__':
    df = read_excel_file('../data/operations.xlsx')
    df = df.fillna(0)
    print(spending_by_category(df, 'Супермаркеты', '2020-05-01 12:00:00'))
#     print(spending_by_category(df, 'Супермаркеты'))
