import json
from unittest import mock

import config
from src.views import main_page


def test_main_page_valid_date():
    """Тестирование возврата JSON-ответа"""
    date_input = "2020-05-20 12:00:00"
    result = main_page(date_input)
    assert json.loads(result)["greeting"] is not None


def test_main_page_json_format():
    """Тестирование возврата JSON-ответа"""
    date_input = "2020-05-20 12:00:00"
    result = main_page(date_input)
    assert json.loads(result) is not None


@mock.patch("src.views.read_excel_file")
@mock.patch("src.views.filter_by_date")
@mock.patch("src.views.get_greeting")
@mock.patch("src.views.get_cards")
@mock.patch("src.views.get_top_trans")
@mock.patch("src.views.get_currency_rates")
@mock.patch("src.views.get_stock_prices")
def test_main_page_function_calls(
    mock_get_stock_prices,
    mock_get_currency_rates,
    mock_get_top_trans,
    mock_get_cards,
    mock_get_greeting,
    mock_filter_by_date,
    mock_read_excel_file,
):
    date_input = "2020-05-20 12:00:00"

    mock_read_excel_file.return_value = {}
    mock_filter_by_date.return_value = {}
    mock_get_greeting.return_value = "Добрый день"
    mock_get_cards.return_value = []
    mock_get_top_trans.return_value = []
    mock_get_currency_rates.return_value = {}
    mock_get_stock_prices.return_value = {}

    main_page(date_input)

    mock_read_excel_file.assert_called_once_with(config.EXCEL_DATA)
    mock_filter_by_date.assert_called_once_with(
        mock_read_excel_file.return_value, date_input
    )
    mock_get_greeting.assert_called_once_with(date_input)
    mock_get_cards.assert_called_once_with(mock_filter_by_date.return_value)
    mock_get_top_trans.assert_called_once_with(mock_filter_by_date.return_value)
    mock_get_currency_rates.assert_called_once_with(config.USER_SETT_PATH)
    mock_get_stock_prices.assert_called_once_with(config.USER_SETT_PATH)
