from src.services import cashback_analysis, df_to_dict


def test_df_to_dict(sample_transactions):
    """Тестирование преобразования датафрейма в список словарей."""
    result = df_to_dict(sample_transactions)
    assert type(result) is list


def test_cashback_analysis(sample_dict):
    """Тестирование фильтрации списка c успешным результатом."""
    result = cashback_analysis(sample_dict, 2022, 1)
    assert result == '{\n    "Category2": 30,\n    "Category1": 20\n}'


def test_cashback_analysis_empty_dict():
    """Тестирование работы функции с пустым списком на входе."""
    data = []
    result = cashback_analysis(data, 2020, 5)
    assert result == []


def test_cashback_analysis_no_cashback(sample_dict_no_cashback):
    """Тестирование работы функции при нулевом значении кэшбэка."""
    result = cashback_analysis(sample_dict_no_cashback, 2022, 1)
    assert result == '{"message": "За 1.2022 кэшбэка нет"}'
