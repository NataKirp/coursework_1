def get_greeting():
    return "Добрый день"

def get_cards():
    return [
    {
      "last_digits": "5814",
      "total_spent": 1262.00,
      "cashback": 12.62
    },
    {
      "last_digits": "7512",
      "total_spent": 7.94,
      "cashback": 0.08
    }
  ]

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
    return {
  "greeting": get_greeting(),
  "cards": get_cards(),
  "top_transactions": get_top_trans(),
  "currency_rates": get_currency_rates(),
  "stock_prices": get_stock_prices()
}


def main_page():
    data = get_data()

    print(data['greeting'])

    for card in data['cards']:
        print(card)

    for trans in data['top_transactions']:
        print(trans)

    for rate in data['currency_rates']:
        print(rate)

    for price in data['stock_prices']:
        print(price)

main_page()