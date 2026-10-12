
# Лабораторна робота №3
# Мінімагазин у консолі

products = {
    1: {"name": "Ноутбук", "price": 25000.00, "stock": 5},
    2: {"name": "Мишка", "price": 450.50, "stock": 20},
    3: {"name": "Клавіатура", "price": 1200.00, "stock": 12},
    4: {"name": "Навушники", "price": 899.99, "stock": 15},
    5: {"name": "Монітор", "price": 6500.00, "stock": 7}
}

cart = {}
ADMIN_PASSWORD = "admin123"


# Форматування ціни
format_price = lambda price: f"{price:.2f} грн"


# Перегляд каталогу
def show_catalog():
    print("\n========== КАТАЛОГ ТОВАРІВ ==========")

    for product_id, product in products.items():
        print(
            f"{product_id}. {product['name']} | "
            f"Ціна: {format_price(product['price'])}"
        )


# Додавання товару в кошик
def add_to_cart():
    show_catalog()

    try:
        product_id = int(input("\nВведіть номер товару: "))

        if product_id not in products:
            print("Такого товару не існує!")
            return

        quantity = int(input("Введіть кількість: "))

        if quantity <= 0:
            print("Кількість повинна бути більшою за 0!")
            return

        product = products[product_id]
        already_in_cart = cart.get(product_id, 0)

        if already_in_cart + quantity > product["stock"]:
            print("Недостатньо товару на складі!")
            return

        cart[product_id] = already_in_cart + quantity
        print("Товар успішно додано до кошика!")

    except ValueError:
        print("Помилка! Введіть ціле число.")


# Перегляд кошика
def show_cart():
    print("\n========== ВАШ КОШИК ==========")

    if not cart:
        print("Кошик порожній.")
        return

    total = 0

    for product_id, quantity in cart.items():
        product = products[product_id]
        subtotal = product["price"] * quantity
        total += subtotal

        print(
            f"{product['name']} | Кількість: {quantity} | "
            f"Сума: {format_price(subtotal)}"
        )

    print("-" * 35)
    print(f"Загальна сума: {format_price(total)}")


# Видалення товару з кошика
def remove_from_cart():
    if not cart:
        print("\nКошик порожній.")
        return

    show_cart()

    try:
        product_id = int(
            input("\nВведіть номер товару для видалення: ")
        )

        if product_id not in cart:
            print("Цього товару немає у кошику!")
            return

        quantity = int(
            input("Скільки одиниць видалити? ")
        )

        if quantity <= 0:
            print("Кількість повинна бути більшою за 0!")
            return

        if quantity >= cart[product_id]:
            del cart[product_id]
            print("Товар повністю видалено з кошика.")
        else:
            cart[product_id] -= quantity
            print("Кількість товару зменшено.")

    except ValueError:
        print("Помилка! Введіть ціле число.")


# Купівля товарів
def buy_products():
    if not cart:
        print("\nНеможливо оформити покупку: кошик порожній.")
        return

    # Додаткова перевірка залишків перед покупкою
    for product_id, quantity in cart.items():
        if quantity > products[product_id]["stock"]:
            print("Покупку скасовано: недостатньо товару.")
            return

    total = sum(
        products[product_id]["price"] * quantity
        for product_id, quantity in cart.items()
    )

    show_cart()

    confirmation = input(
        "\nПідтвердити покупку? (так/ні): "
    ).strip().lower()

    if confirmation not in ("так", "т", "yes", "y"):
        print("Покупку скасовано.")
        return

    # Зменшуємо залишки на складі
    for product_id, quantity in cart.items():
        products[product_id]["stock"] -= quantity

    cart.clear()

    print("\nПокупку успішно оформлено!")
    print(f"До сплати: {format_price(total)}")
    print("Дякуємо за покупку!")


# Вхід адміністратора
def admin_login():
    password = input("\nВведіть пароль адміністратора: ")

    if password != ADMIN_PASSWORD:
        print("Неправильний пароль!")
        return

    print("\n========== ПАНЕЛЬ АДМІНІСТРАТОРА ==========")
    print("Залишки товарів на складі:")

    # Лямбда-функція для сортування за назвою
    sorted_products = sorted(
        products.items(),
        key=lambda item: item[1]["name"]
    )

    for product_id, product in sorted_products:
        print(
            f"{product['name']} | "
            f"Ціна: {format_price(product['price'])} | "
            f"Залишок: {product['stock']} шт."
        )

    # Лямбда-функція для пошуку товарів, що закінчуються
    low_stock = list(
        filter(
            lambda item: item[1]["stock"] <= 5,
            products.items()
        )
    )

    print("\nТовари, яких залишилося 5 або менше:")

    if low_stock:
        for product_id, product in low_stock:
            print(f"{product['name']}: {product['stock']} шт.")
    else:
        print("Усі товари є в достатній кількості.")


# Головне меню
def main():
    while True:
        print("\n========== МІНІМАГАЗИН ==========")
        print("1. Переглянути каталог")
        print("2. Додати товар у кошик")
        print("3. Переглянути кошик")
        print("4. Видалити товар із кошика")
        print("5. Купити товари")
        print("6. Увійти як адміністратор")
        print("0. Вихід")

        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            show_catalog()
        elif choice == "2":
            add_to_cart()
        elif choice == "3":
            show_cart()
        elif choice == "4":
            remove_from_cart()
        elif choice == "5":
            buy_products()
        elif choice == "6":
            admin_login()
        elif choice == "0":
            print("Дякуємо за відвідування магазину!")
            break
        else:
            print("Невірний пункт меню. Спробуйте ще раз.")


# Запуск програми
if __name__ == "__main__":
    main()
