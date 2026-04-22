import pytest

from src.services import df_to_dict, cashback_analysis


# Тестирование преобразования датафрейма в список словарей
def test_df_to_dict(sample_transactions):
    result = df_to_dict(sample_transactions)
    assert type(result) == list


# Тестирование фильтрации списка c успешным результатом
def test_cashback_analysis(sample_dict):
    result = cashback_analysis(sample_dict, 2022, 1)
    assert result == '{\n    "Category2": 30,\n    "Category1": 20\n}'

# Тестирование работы функции с пустым списком на входе
def test_cashback_analysis_empty_dict():
    data = []
    result = cashback_analysis(data, 2020, 5)
    assert result == []

#  Тестирование работы функции при нулевом значении кэшбэка
def test_cashback_analysis_no_cashback(sample_dict_no_cashback):
    result = cashback_analysis(sample_dict_no_cashback, 2022, 1)
    assert result == '{"message": "За 1.2022 кэшбэка нет"}'
