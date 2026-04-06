import datetime

import pandas as pd
from pandas import DataFrame


def get_greeting()->str:
    """
    Функция для вывода приветствия в зависимости от времени суток
    :return:
    """
    now = datetime.datetime.now()
    if now.hour in range(6, 12):
        return "Доброе утро"
    elif now.hour in range(12, 18):
        return "Добрый день"
    elif now.hour in range(18, 00):
        return "Добрый вечер"
    elif now.hour in range(00, 6):
        return "Доброй ночи"


def read_excel_file(file_path: str) -> DataFrame:
    """
    Функция для считывания финансовых операций из Excel файла
    :param file_path: Путь к файлу Excel
    :return: Список словарей с транзакциями
    """
    df = pd.read_excel(file_path)
    return df


def get_cards():
    """
    Функция для агрегации данных по номеру карты
    :return:
    """
    df = read_excel_file('../data/operations.xlsx')

    card_data_sorted = df[
        [
            'Номер карты',
            'Сумма операции',
            'Кэшбэк'
        ]
    ]
    grouped_by_card = card_data_sorted.groupby('Номер карты')

    cards = []

    for card, data in grouped_by_card:
        total_spent = data['Сумма операции'].sum()
        cashback = data["Кэшбэк"].sum()
        card_data = {
            'last_digits': card,
            'total_spent':round(total_spent, 2),
            'cashback': cashback
        }
        cards.append(card_data)

    return cards