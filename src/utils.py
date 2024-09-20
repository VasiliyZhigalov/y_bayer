import re
def parse_shopping_list(message: str):
    # Регулярное выражение для более свободного формата, например "Milk: 2" или "Bread - 1"
    pattern = r'([A-Za-zА-Яа-я\s]+)[:\-\s]+(\d+)'

    items = []

    # Ищем все соответствия паттерну
    for match in re.finditer(pattern, message):
        item_name = match.group(1).strip()
        quantity = int(match.group(2))

        items.append({
            "name": item_name,
            "quantity": quantity
        })

    return items


