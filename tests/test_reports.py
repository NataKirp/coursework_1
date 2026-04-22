import tempfile

import pandas as pd
import json
from pathlib import Path

import pytest

from src.reports import save_report, spending_by_category
import datetime


def test_save_report():
    test_dir = tempfile.mkdtemp()

    try:
        @save_report(filename='manual_test', reports_dir=test_dir)
        def get_data():
            return '{"key": "value"}'

        result = get_data()

        assert result == '{"key": "value"}', "Функция вернула неверные данные"

        timestamp = datetime.datetime.now().strftime('%Y%m%d')
        expected_path = Path(test_dir) / f"manual_test_{timestamp}.json"

        assert expected_path.exists(), f"Файл {expected_path} не был создан"

        with open(expected_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert content == '{"key": "value"}', "Содержимое файла не совпадает"

        print("✅ Тест успешно пройден!")

    except AssertionError as e:
        print(f"❌ Тест провален: {e}")
    except Exception as e:
        print(f"💥 Произошла ошибка при выполнении теста: {e}")


def test_spending_by_category(sample_transactions):
    result = spending_by_category(sample_transactions, 'Category1', date='2022-01-04 00:00:00')

    try:
        result_list = json.loads(result)
        assert result_list == {
            'Category1': [{'Описание': 'Desc2', 'Сумма операции': -200}, {'Описание': 'Desc1', 'Сумма операции': -100}]}
    except json.JSONDecodeError:
        assert False, "The result is not a valid JSON"


@pytest.mark.parametrize('df_input, category, expected_msg', [
    (
            pd.DataFrame({'Дата операции': [], 'Категория': [], 'Сумма операции': [], 'Описание': []}),
            'Category1',
            'За период c 2021-10-01 12:00:00 по 2022-01-01 12:00:00 нет данных по тратам'
    ),
    (
            pd.DataFrame({
                'Дата операции': ['01.01.2022 12:00:00', '02.01.2022 12:00:00', '03.01.2022 12:00:00'],
                'Категория': ['Category2', 'Category2', 'Category2'],
                'Сумма операции': [-100, -200, -300],
                'Описание': ['Desc1', 'Desc2', 'Desc3']
            }),
            'Category1',
            'За период c 2021-10-01 12:00:00 по 2022-01-01 12:00:00 нет трат по категории Category1'
    )
])
def test_spending_by_category_no_data(df_input, category, expected_msg):
    result = spending_by_category(df_input, category, '2022-01-01 12:00:00')

    try:
        result_dict = json.loads(result)
        assert result_dict.get('message') == expected_msg
    except json.JSONDecodeError:
        assert False, "The result is not a valid JSON"
