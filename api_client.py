"""
Модуль для работы с API курса валют.
Содержит функции для получения данных из exchangerate-api.com
"""

import requests  # type: ignore
from typing import Optional, Dict, Any

# Список основных валют для обновления
FAVORITE_CURRENCIES = ["USD", "EUR", "GBP", "RUB"]


def get_currency_rate(currency_code: str) -> Optional[Dict[str, Any]]:
    """
    Получить курс валюты относительно базовой валюты из API.

    Args:
        currency_code (str): Код базовой валюты (например, 'USD')

    Returns:
        Optional[Dict[str, Any]]: Словарь с данными о курсах или None при ошибке
    """
    URL = f"https://open.er-api.com/v6/latest/{currency_code}"

    try:
        response = requests.get(URL, timeout=10)
        if response.status_code != 200:
            print(f"Ошибка HTTP {response.status_code}: {response.text}")
            return None

        data = response.json()
        if data.get('result') != 'success':
            print(f"Ошибка API: {data.get('error-type', 'Неизвестная ошибка')}")
            return None

        return data

    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


def update_currency_rates() -> Dict[str, Any]:
    """
    Обновить курсы всех основных валют и вернуть собранные данные.

    Returns:
        Dict[str, Any]: Словарь с данными о курсах валют
    """
    all_data = {}
    success_count = 0

    print("Получение курсов валют...")

    for currency in FAVORITE_CURRENCIES:
        print(f"  Получение данных для {currency}...")
        rate_data = get_currency_rate(currency)

        if rate_data:
            all_data[currency] = rate_data
            success_count += 1
        else:
            print(f"  Не удалось получить данные для {currency}")

    print(f"Успешно получено данных для {success_count}/{len(FAVORITE_CURRENCIES)} валют")
    return all_data
