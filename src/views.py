import json

from src.utils import get_greeting, get_cards


def get_top_trans():
    return [
        {
            "date": "21.12.2021",
            "amount": 1198.23,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR"
        },
        {
            "date": "20.12.2021",
            "amount": 829.00,
            "category": "Супермаркеты",
            "description": "Лента"
        },
        {
            "date": "20.12.2021",
            "amount": 421.00,
            "category": "Различные товары",
            "description": "Ozon.ru"
        },
        {
            "date": "16.12.2021",
            "amount": -14216.42,
            "category": "ЖКХ",
            "description": "ЖКУ Квартира"
        },
        {
            "date": "16.12.2021",
            "amount": 453.00,
            "category": "Бонусы",
            "description": "Кешбэк за обычные покупки"
        }
    ]


def get_currency_rates():
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


def get_stock_prices():
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


def get_data():
    main_data = {
        "greeting": get_greeting(),
        "cards": get_cards(),
        "top_transactions": get_top_trans(),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices()
    }
    print(json.dumps(main_data, indent=4, ensure_ascii=False))


get_data()

# def main_page():
#     main_data = get_data()
#
#     print(main_data['greeting'])
#
#     for card in main_data['cards']:
#         print(json.dumps(card, indent=4, ensure_ascii=False))
#
#     for trans in main_data['top_transactions']:
#         print(trans)
#
#     for rate in main_data['currency_rates']:
#         print(rate)
#
#     for price in main_data['stock_prices']:
#         print(price)
#
# main_page()
