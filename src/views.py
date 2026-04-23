import json

import config
from src.utils import (filter_by_date, get_cards, get_currency_rates,
                       get_greeting, get_stock_prices, get_top_trans,
                       read_excel_file)


def main_page(date_input: str) -> str:
    """
    Функция для страницы 'Главная' для вывода приветствия, сводных данных о транзакциях, текущих курсов валют и акций.
    """
    df = read_excel_file(config.EXCEL_DATA)  # видео 3 время 11:40
    df_filtered = filter_by_date(df, date_input)
    main_data = {
        "greeting": get_greeting(date_input),
        "cards": get_cards(df_filtered),
        "top_transactions": get_top_trans(df_filtered),
        "currency_rates": get_currency_rates(config.USER_SETT_PATH),
        "stock_prices": get_stock_prices(config.USER_SETT_PATH),
    }
    return json.dumps(main_data, indent=4, ensure_ascii=False)
