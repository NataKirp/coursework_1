import json

import config
from src.utils import get_greeting, get_cards, read_excel_file, filter_by_date, get_top_trans, get_currency_rates, \
    get_stock_prices


def main_page(date_input: str) -> str:
    """Функция для страницы 'Главная' для вывода приветствия, сводных данных о транзакциях, текущих курсов валют и акций."""
    df = read_excel_file(config.EXCEL_DATA)  # видео 3 время 11:40
    df_filtered = filter_by_date(df, date_input)
    main_data = {
        "greeting": get_greeting(date_input),
        "cards": get_cards(df_filtered),
        "top_transactions": get_top_trans(df_filtered),
        "currency_rates": get_currency_rates(config.USER_SETT_PATH),
        "stock_prices": get_stock_prices(config.USER_SETT_PATH)
    }
    return json.dumps(main_data, indent=4, ensure_ascii=False)


# if __name__ == '__main__':
#     main_page('2020-05-20 20:00:00')
