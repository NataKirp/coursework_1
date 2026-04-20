import json
from collections import defaultdict
from datetime import datetime

from pandas import DataFrame

from src.utils import read_excel_file


def df_to_dict(df: DataFrame) -> list[dict]:
    data_list = df.to_dict(orient='records')
    return data_list


def cashback_analysis(data: list[dict], year: int, month: int):
    """Функция для анализа выгодности категорий повышенного кэшбэка."""
    filtered_by_month_year = [
        item for item in data
        if (d := datetime.strptime(item['Дата операции'], '%d.%m.%Y %H:%M:%S')).month == month
           and d.year == year
    ]

    filtered_by_category = defaultdict(int)
    for item in filtered_by_month_year:
        filtered_by_category[item['Категория']] += item['Кэшбэк']

    sorted_by_category = dict(sorted(filtered_by_category.items(), key=lambda x: x[1], reverse=True))
    # округляем значения кэшбэка и исключаем значения, где кэшбэк 0
    sorted_by_category = {k: round(v) for k, v in sorted_by_category.items() if round(v) != 0}

    json_output = json.dumps(sorted_by_category, indent=4, ensure_ascii=False)

    return json_output

# if __name__ == '__main__':
#     df = read_excel_file('../data/operations.xlsx')
#     df = df.fillna(0)
#     data = df_to_dict(df)
#     print(cashback_analysis(data, 2018, 3))
