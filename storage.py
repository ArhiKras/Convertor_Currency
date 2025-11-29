"""
Модуль для работы с хранением данных.
Содержит функции для чтения/записи файлов и управления кэшем данных.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from api_client import update_currency_rates, FAVORITE_CURRENCIES


def save_to_file(data: Dict[str, Any], filename: str = 'currency.json') -> None:
    """
    Сохранить данные в JSON файл.

    Args:
        data (Dict[str, Any]): Данные для сохранения
        filename (str): Имя файла (по умолчанию 'currency.json')
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"✓ Данные сохранены в файл {filename}")
    except Exception as e:
        print(f"❌ Ошибка сохранения файла {filename}: {e}")


def read_from_file(filename: str = 'currency.json') -> Optional[Dict[str, Any]]:
    """
    Прочитать данные из JSON файла.

    Args:
        filename (str): Имя файла для чтения

    Returns:
        Optional[Dict[str, Any]]: Данные из файла или None при ошибке
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения JSON из файла {filename}: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла {filename}: {e}")
        return None


def is_file_recent(file_path: str, hours: int = 24) -> bool:
    """
    Проверить, существует ли файл и моложе ли он указанного количества часов.

    Args:
        file_path (str): Путь к файлу
        hours (int): Количество часов для проверки актуальности

    Returns:
        bool: True если файл существует и моложе указанного времени
    """
    if not os.path.exists(file_path):
        return False

    try:
        # Получаем время последнего изменения файла
        file_time = os.path.getmtime(file_path)
        file_datetime = datetime.fromtimestamp(file_time)

        # Проверяем, прошло ли меньше часов с момента изменения
        return datetime.now() - file_datetime < timedelta(hours=hours)
    except Exception as e:
        print(f"Ошибка проверки возраста файла {file_path}: {e}")
        return False


def load_or_update_data(filename: str = 'currency.json') -> Optional[Dict[str, Any]]:
    """
    Загрузить данные из файла или обновить их из API.

    Args:
        filename (str): Имя файла для кэширования данных

    Returns:
        Optional[Dict[str, Any]]: Загруженные или обновленные данные
    """
    if is_file_recent(filename, 24):
        try:
            data = read_from_file(filename)
            if data:
                print("✓ Данные о курсах загружены из файла (актуальны)")
                return data
            else:
                print("⚠ Ошибка чтения файла, будет выполнено обновление данных...")
        except Exception as e:
            print(f"⚠ Ошибка чтения файла: {e}")
            print("Будет выполнено обновление данных...")

    # Файл не существует, старый или ошибка чтения - обновляем данные
    print("Обновление данных о курсах...")
    all_data = update_currency_rates()

    if all_data:
        save_to_file(all_data, filename)
        print("✓ Данные обновлены и загружены")
        return all_data
    else:
        print("❌ Не удалось получить данные из API")
        return None


def get_available_currencies() -> list:
    """Получить список всех доступных валют из файла"""
    try:
        data = read_from_file()
        if not data:
            return []

        # Возьмем валюты из первой доступной базовой валюты
        first_base = list(data.keys())[0]
        return list(data[first_base]['rates'].keys())
    except Exception:
        return []


def get_exchange_rate(base_currency: str, target_currency: str):
    """Получить курс обмена между двумя валютами"""
    try:
        data = read_from_file()
        if not data or base_currency not in data:
            return None, f"Базовая валюта {base_currency} не найдена"

        rates = data[base_currency]['rates']
        if target_currency not in rates:
            return None, f"Целевая валюта {target_currency} не найдена"

        return rates[target_currency], None
    except Exception as e:
        return None, f"Ошибка при получении курса: {str(e)}"


def convert_currency(amount: float, base_currency: str, target_currency: str):
    """Конвертировать сумму из одной валюты в другую"""
    rate, error = get_exchange_rate(base_currency, target_currency)
    if error:
        return None, error

    converted_amount = amount * rate
    return converted_amount, None
