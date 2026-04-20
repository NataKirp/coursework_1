import json
import datetime
from typing import Optional, List, Any

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import read_excel_file


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> list[Any] | str:
    if date is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    start_date = end_date - relativedelta(months=3)

    filtered_by_date = transactions[
        (transactions['Дата операции'] >= start_date) & (transactions['Дата операции'] <= end_date)]

    if filtered_by_date is None or filtered_by_date.empty:
        print('Нет данных за период')
        return []

    filtered_by_category = filtered_by_date[filtered_by_date['Категория'] == category]

    grouped = filtered_by_category.groupby('Описание')['Сумма операции'].sum().reset_index()
    grouped = grouped.sort_values(by='Сумма операции', ascending=True)  # True, т.к. суммы отрицательные, по убыванию
    # создаем словарь под каждое описание
    output_list = grouped.to_dict(orient='records')
    output = {category: output_list}
    json_output = json.dumps(output, indent=4, ensure_ascii=False)

    return json_output

# if __name__ == '__main__':
#     df = read_excel_file('../data/operations.xlsx')
#     df = df.fillna(0)
#     print(spending_by_category(df, 'Супермаркеты', '2020-05-01 12:00:00'))
#     print(spending_by_category(df, 'Супермаркеты'))
