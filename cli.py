"""
Модуль интерфейса командной строки для конвертера валют.
Содержит функции для взаимодействия с пользователем.
"""

from storage import (
    load_or_update_data,
    get_available_currencies,
    get_exchange_rate,
    convert_currency,
    update_currency_rates
)


def display_available_currencies():
    """Показать доступные валюты в удобном формате"""
    currencies = get_available_currencies()
    if not currencies:
        print("Нет доступных валют")
        return

    print(f"\nДоступные валюты ({len(currencies)}):")
    print("-" * 50)

    # Разделим на группы по 10 валют для лучшей читаемости
    for i in range(0, len(currencies), 10):
        group = currencies[i:i+10]
        print(" ".join(f"{code:>4}" for code in group))
    print("-" * 50)


def show_menu():
    """Показать главное меню программы"""
    print("\n" + "="*50)
    print("КОНВЕРТЕР ВАЛЮТ")
    print("="*50)
    print("1. Конвертировать валюту")
    print("2. Показать курс обмена")
    print("3. Показать доступные валюты")
    print("4. Обновить данные о курсах")
    print("5. Найти валюту по коду")
    print("0. Выход")
    print("="*50)


def get_valid_currency(prompt: str):
    """Получить корректный код валюты от пользователя"""
    while True:
        currency = input(prompt).strip().upper()
        if not currency:
            print("Код валюты не может быть пустым")
            continue

        available = get_available_currencies()
        if currency in available:
            return currency
        else:
            print(f"Валюта {currency} не найдена. Попробуйте еще раз.")


def get_valid_amount():
    """Получить корректную сумму от пользователя"""
    while True:
        try:
            amount = float(input("Введите сумму: "))
            if amount <= 0:
                print("Сумма должна быть положительной")
                continue
            return amount
        except ValueError:
            print("Некорректная сумма. Введите число.")


def currency_conversion_interface():
    """Интерфейс для конвертации валют"""
    print("\nКОНВЕРТАЦИЯ ВАЛЮТ")

    # Выбор базовой валюты
    base_currency = get_valid_currency("Введите код базовой валюты (например, USD): ")

    # Выбор целевой валюты
    target_currency = get_valid_currency("Введите код целевой валюты (например, EUR): ")

    # Ввод суммы
    amount = get_valid_amount()

    # Конвертация
    converted_amount, error = convert_currency(amount, base_currency, target_currency)

    if error:
        print(f"Ошибка: {error}")
    else:
        print(f"\nРезультат конвертации:")
        print(f"{amount:.2f} {base_currency} = {converted_amount:.2f} {target_currency}")

        # Показать обратный курс
        reverse_rate, _ = get_exchange_rate(target_currency, base_currency)
        if reverse_rate:
            print(f"Обратный курс: 1 {target_currency} = {reverse_rate:.4f} {base_currency}")


def exchange_rate_interface():
    """Интерфейс для просмотра курса обмена"""
    print("\nКУРС ОБМЕНА")

    base_currency = get_valid_currency("Введите код базовой валюты: ")
    target_currency = get_valid_currency("Введите код целевой валюты: ")

    rate, error = get_exchange_rate(base_currency, target_currency)

    if error:
        print(f"Ошибка: {error}")
    else:
        print(f"\nКурс обмена:")
        print(f"1 {base_currency} = {rate:.4f} {target_currency}")


def search_currency_interface():
    """Интерфейс для поиска валюты"""
    print("\nПОИСК ВАЛЮТЫ")
    search_term = input("Введите код валюты для поиска: ").strip().upper()

    available = get_available_currencies()
    found = [currency for currency in available if search_term in currency]

    if found:
        print(f"\nНайдено валют ({len(found)}):")
        for currency in sorted(found):
            print(f"  {currency}")
    else:
        print(f"Валюты с кодом '{search_term}' не найдены")


def main():
    """Главная функция программы"""
    print("Добро пожаловать в Конвертер Валют!")

    # Загружаем или обновляем данные автоматически
    data = load_or_update_data()

    if data is None:
        print("❌ Невозможно загрузить данные. Программа будет работать в ограниченном режиме.")

    while True:
        show_menu()
        choice = input("Выберите действие (0-5): ").strip()

        if choice == "0":
            print("До свидания!")
            break
        elif choice == "1":
            currency_conversion_interface()
        elif choice == "2":
            exchange_rate_interface()
        elif choice == "3":
            display_available_currencies()
        elif choice == "4":
            print("Принудительное обновление данных...")
            update_currency_rates()
            print("✓ Данные успешно обновлены")
        elif choice == "5":
            search_currency_interface()
        else:
            print("Некорректный выбор. Попробуйте еще раз.")

        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()
