import datetime
import json
import os
import time
from pathlib import Path

import pandas as pd
import requests
from pandas import DataFrame
from dotenv import load_dotenv

import config
from src.logging_config import setup_logging

load_dotenv()

utils_logger = setup_logging('utils')


def get_greeting(date_input: str = None) -> str:
    """Функция для вывода приветствия в зависимости от времени суток."""
    if not date_input:
        date_input = datetime.datetime.now()
    else:
        date_input = datetime.datetime.strptime(date_input, '%Y-%m-%d %H:%M:%S')
    if date_input.hour in range(6, 12):
        return "Доброе утро"
    elif date_input.hour in range(12, 18):
        return "Добрый день"
    elif date_input.hour in range(18, 24):
        return "Добрый вечер"
    elif date_input.hour in range(24, 6):
        return "Доброй ночи"


def read_excel_file(file_path: Path) -> DataFrame:
    """Функция для считывания успешных финансовых операций (статус ОК) из Excel файла."""
    utils_logger.info(f'Начало работы функции "read_excel_file".')

    path = Path(file_path)   # превращаем в объект Path если пришла строка

    if not path.exists():
        utils_logger.error(f'Файл не найден: {path}.')
        raise FileNotFoundError(f'файл по пути {path} не найден.')

    if path.suffix != '.xlsx':
        utils_logger.error(f'Неверный формат файла {path.suffix}.')
        raise ValueError(f'Файл должен иметь формат .xlsx.')

    try:
        df = pd.read_excel(path)
        df_from_excel = df[df['Статус'] == 'OK']
        return df_from_excel
    except Exception as e:
        utils_logger.exception(f'Произошла ошибка при чтении файла: {e}')
        raise
    finally:
        utils_logger.info(f'Завершение работы функции "read_excel_file".')


def filter_by_date(data: DataFrame, date_input: str = None) -> DataFrame:
    """Функция для отбора данных из датафрейма за определенный период."""
    utils_logger.info(f'Начало работы функции "filter_by_date".')
    if date_input is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(date_input, '%Y-%m-%d %H:%M:%S')

    data['Дата операции'] = pd.to_datetime(data['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    start_date = end_date.replace(day=1)

    df_filtered = data[(data['Дата операции'] >= start_date) & (data['Дата операции'] <= end_date)]
    utils_logger.info(f'Завершение работы функции "filter_by_date".')

    return df_filtered


def get_cards(data: DataFrame) -> list[dict]:
    """Функция для агрегации данных по номеру карты"""
    utils_logger.info(f'Начало работы функции "get_cards".')
    if data is None or data.empty:
        utils_logger.warning('В датафрейме нет данных.')
        return []
    card_data_sorted = data[
        [
            'Номер карты',
            'Сумма операции',
            'Кэшбэк'
        ]
    ]
    grouped_by_card = card_data_sorted.groupby('Номер карты')

    cards = []
    for card, group_data in grouped_by_card:
        total_spent = data['Сумма операции'].sum()
        cashback = data["Кэшбэк"].sum()
        card_data = {
            'last_digits': card,
            'total_spent': round(total_spent, 2),
            'cashback': cashback
        }
        cards.append(card_data)
        utils_logger.info(f'Завершение работы функции "get_cards".')

    return cards


def get_top_trans(data: DataFrame, top: int = 5) -> dict | list[dict]:
    """Функция для фильтрации топ N (по умолчанию 5) транзакций по сумме платежа."""
    utils_logger.info(f'Начало работы функции "get_top_trans".')
    if data is None or data.empty:
        utils_logger.warning('В датафрейме нет данных.')
        return []
    df_top_amount = data.sort_values(by='Сумма операции', key=lambda x: x.abs(), ascending=False)
    result = df_top_amount.head(top)
    result['Дата операции'] = result['Дата операции'].astype(str)  # для последующего вывода в формате JSON-ответа
    result_rename = result[['Дата операции', 'Сумма операции', 'Категория', 'Описание']].rename(columns={
        'Дата операции': 'date',
        'Сумма операции': 'amount',
        'Категория': 'category',
        'Описание': 'description'
    })
    result_dict = result_rename[['date', 'amount', 'category', 'description']].to_dict(orient='records')
    utils_logger.info(f'Завершение работы функции "get_top_trans".')

    return result_dict


# def get_currency_rates(path_to_json: Path) -> list[dict]:
#     """Функция для получения курсов валют с сервиса APILayer."""
#     utils_logger.info(f'Начало работы функции "get_currency_rates".')
#
#     path = Path(path_to_json)  # превращаем в объект Path если пришла строка
#
#     currency_rates = []
#     date = datetime.datetime.now()
#     date_str = date.strftime('%Y-%m-%d')
#     with open(path_to_json, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         currencies = data['user_currencies']
#         utils_logger.info(f'Получение курсов валют {currencies} с APILayer.')
#         for currency in currencies:
#             try:
#                 url = f"https://api.apilayer.com/currency_data/historical?date={date_str}&currencies=RUB&source={currency}"
#                 payload = {}
#                 api_key = os.getenv("APILAYER_API_KEY")
#                 headers = {"apikey": api_key}
#                 response = requests.request("GET", url, headers=headers, data=payload)
#                 response.raise_for_status()  # возвращаем исключение если код ошибки не 200
#                 result = response.json()
#                 # используем iter() для создания итератора по значениям словаря и next() для получения первого значения,
#                 # т.к. всегда одна пара ключ-значение
#
#                 if 'quotes' in result:
#                     currency_rate = round(next(iter(result['quotes'].values())), 2)
#                     currency_rates.append({
#                         "currency": currency,
#                         "rate": currency_rate
#                     })
#                     utils_logger.info(f"Успешно: {currency} - {currency_rate}")
#                 elif "Note" in result:
#                     utils_logger.warning(f"Лимит запросов превышен для {currency}. Ждем дольше...")
#                 else:
#                     utils_logger.warning(f"Ошибка при получении данных для {currency}.")
#
#
#                 if currency != currencies[-1]:  # добавляем паузу после каждого запроса, кроме последнего
#                     wait_time = 15 # ждем 15 сек
#                     utils_logger.info(f"Ожидание {wait_time} сек. перед следующим запросом...")
#                     time.sleep(wait_time)
#
#             except requests.RequestException as e:
#                 utils_logger.exception(f'Ошибка запроса: Код: {e}')
#                 print(f'Ошибка запроса: Код: {e}')
#         utils_logger.info(f'Завершение работы функции "get_currency_rates".')
#
#         return currency_rates


# def get_stock_prices(path_to_json: Path) -> list[dict]:
#     """Функция для получения стоимости акций из S&P500 с сервиса Alpha Vantage."""
#     utils_logger.info(f'Начало работы функции "get_stock_prices".')
#
#     path = Path(path_to_json)  # превращаем в объект Path если пришла строка
#
#     with open(path_to_json, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         stocks = data['user_stocks']
#         stock_prices = []
#
#         utils_logger.info(f'Получение курсов акций {stocks} с Alpha Vantage.')
#         for stock in stocks:
#             try:
#                 apikey = os.getenv("ALFA_VANTAGE_API_KEY")
#                 url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&outputsize=compact&apikey={apikey}'
#                 r = requests.get(url)
#                 r.raise_for_status()  # возвращаем исключение если код ошибки не 200
#                 stocks_data = r.json()
#                 if 'Meta Data' in stocks_data:
#                     date = stocks_data['Meta Data']['3. Last Refreshed']
#                     stock_price = stocks_data['Time Series (Daily)'][date]['4. close']
#                     stock_prices.append({
#                         "stock": stock,
#                         "price": float(stock_price)
#                     })
#                     utils_logger.info(f"Успешно: {stock} - {stock_price}")
#                 elif "Note" in stocks_data:
#                     utils_logger.warning(f"Лимит запросов превышен для {stock}. Ждем дольше...")
#                 else:
#                     utils_logger.warning(f"Ошибка при получении данных для {stock}.")
#             except requests.RequestException as e:
#                 utils_logger.exception(f'Ошибка запроса: Код: {e}')
#                 print(f"Ошибка запроса: Код: {e}")
#
#
#             if stock != stocks[-1]:  # добавляем паузу после каждого запроса, кроме последнего
#                 wait_time = 15  # ждем 15 сек
#                 utils_logger.info(f"Ожидание {wait_time} сек. перед следующим запросом...")
#                 time.sleep(wait_time)
#
#         utils_logger.info(f'Завершение работы функции "get_stock_prices".')
#
#         return stock_prices


def get_currency_rates(path_to_json: Path) -> list[dict]:
    """Функция для получения курсов валют с сервиса APILayer."""
    path = Path(path_to_json)  # превращаем в объект Path если пришла строка


    return [
        {
            "currency": "USD",
            "rate": 73.21
        },
        {
            "currency": "EUR",
            "rate": 87.08
        }
    ]


def get_stock_prices(path_to_json: str) -> list[dict]:
    return [
        {
            "stock": "AAPL",
            "price": 150.12
        },
        {
            "stock": "AMZN",
            "price": 3173.18
        },
        {
            "stock": "GOOGL",
            "price": 2742.39
        },
        {
            "stock": "MSFT",
            "price": 296.71
        },
        {
            "stock": "TSLA",
            "price": 1007.08
        }
    ]

# if __name__ == '__main__':
# date_input = '2020-05-20 12:00:00'
# df = read_excel_file('operations.xlsx')
# df = read_excel_file(config.EXCEL_DATA)
# print(dict(df))
# print(df.head())
# df_filtered = filter_by_date(df)
#
#
# print(get_greeting('2026-04-07 19:00:00'))
# print(get_greeting())
#
# print(get_cards(df_filtered))
# print(filter_by_date(df, '2020-05-20 12:00:00'))
# print(get_top_trans(df_filtered, 2))
#
# print(get_currency_rates(config.USER_SETT_PATH))
# print(get_stock_prices(config.USER_SETT_PATH))
