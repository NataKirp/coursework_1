import datetime
import json
import os

import pandas as pd
import requests
from pandas import DataFrame
from dotenv import load_dotenv

load_dotenv()


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


def read_excel_file(file_path: str) -> DataFrame:
    """Функция для считывания успешных финансовых операций (статус ОК) из Excel файла."""
    df = pd.read_excel(file_path)
    df_from_excel = df[df['Статус'] == 'OK']
    return df_from_excel


def filter_by_date(data: DataFrame, date_input: str = None) -> DataFrame:
    """Функция для отбора данных из датафрейма за определенный период."""
    if date_input is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(date_input, '%Y-%m-%d %H:%M:%S')

    data['Дата операции'] = pd.to_datetime(data['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    start_date = end_date.replace(day=1)

    df_filtered = data[(data['Дата операции'] >= start_date) & (data['Дата операции'] <= end_date)]

    return df_filtered


def get_cards(data: DataFrame) -> list[dict]:
    """Функция для агрегации данных по номеру карты"""
    if data is None or data.empty:
        print('Нет данных за период')
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
    return cards


def get_top_trans(data: DataFrame, top: int = 5) -> dict | list[dict]:
    """Функция для фильтрации топ N (по умолчанию 5) транзакций по сумме платежа."""
    if data is None or data.empty:
        print('Нет данных за период')
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
    return result_dict


def get_currency_rates(path_to_json: str) -> list[dict]:
    """Функция для получения курсов валют с сервиса APILayer."""
    currency_rates = []
    date = datetime.datetime.now()
    date_str = date.strftime('%Y-%m-%d')
    with open(path_to_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
        currencies = data['user_currencies']
        for currency in currencies:
            try:
                url = f"https://api.apilayer.com/currency_data/historical?date={date_str}&currencies=RUB&source={currency}"
                payload = {}
                api_key = os.getenv("APILAYER_API_KEY")
                headers = {"apikey": api_key}
                response = requests.request("GET", url, headers=headers, data=payload)
                response.raise_for_status()  # возвращаем исключение если код ошибки не 200
                result = response.json()
                # используем iter() для создания итератора по значениям словаря и next() для получения первого значения,
                # т.к. всегда одна пара ключ-значение
                currency_rate = round(next(iter(result['quotes'].values())), 2)
                currency_rates.append({
                    "currency": currency,
                    "rate": currency_rate
                })
            except requests.RequestException as e:
                print(f"Ошибка запроса: Код: {e}")
        return currency_rates


# def get_stock_prices(path_to_json: str) -> list[dict]:
#     """Функция для получения стоимости акций из S&P500 с сервиса Alpha Vantage."""
#     with open(path_to_json, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         stocks = data['user_stocks']
#         stock_prices = []
#         date = datetime.datetime.now()
#         date_str = date.strftime('%Y-%m-%d')
#         for stock in stocks:
#             try:
#                 apikey = os.getenv("ALFA_VANTAGE_API_KEY")
#                 url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&outputsize=compact&apikey={apikey}'
#                 r = requests.get(url)
#                 r.raise_for_status()  # возвращаем исключение если код ошибки не 200
#                 stocks_data = r.json()
#                 if 'Time Series (Daily)' in stocks_data:
#                     time_series = stocks_data['Time Series (Daily)']
#                     if date_str in time_series:
#                         stock_price = time_series[date_str]['4. close']
#                         stock_prices.append({
#                             "stock": stock,
#                             "price": stock_price})
#             except requests.RequestException as e:
#                 print(f"Ошибка запроса: Код: {e}")
#         return stock_prices


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
# df = read_excel_file('../data/operations.xlsx')
# print(dict(df))
# print(df.head())
# df_filtered = filter_by_date(df)

#
#     print(get_greeting('2026-04-07 19:00:00'))
#     print(get_greeting())
#
# print(get_cards(df_filtered))
#     print(filter_by_date(df, '2020-05-20 12:00:00'))
#     print(get_top_trans(df_filtered, 2))
#
#     print(get_currency_rates('../user_settings.json'))
#     print(get_stock_prices('../user_settings.json'))
