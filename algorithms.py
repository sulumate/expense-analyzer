"""Алгоритмы на чистом Python, без библиотек."""

KEYWORDS = {
    "magnum": "Продукты",
    "small": "Продукты",
    "такси": "Транспорт",
    "автобус": "Транспорт",
    "кофе": "Кафе",
    "обед": "Кафе",
    "подписка": "Подписки",
    "аптека": "Здоровье",
    "kino": "Развлечения",
    "одежда": "Покупки",
    "коммунальные": "Счета",
}


def categorize(description):
    """Находит категорию по ключевому слову в описании.

    Сложность: O(k), где k - число ключевых слов.
    """
    text = description.lower()
    for keyword, category in KEYWORDS.items():
        if keyword in text:
            return category
    return "Другое"


def merge_sort(items, key):
    """Сортировка слиянием. Сложность: O(n log n) по времени, O(n) по памяти."""
    if len(items) <= 1:
        return items
    middle = len(items) // 2
    left = merge_sort(items[:middle], key)
    right = merge_sort(items[middle:], key)

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def binary_search_first(items, target, key):
    """Индекс первого элемента с key(item) >= target в отсортированном списке.

    Сложность: O(log n).
    """
    low, high = 0, len(items)
    while low < high:
        middle = (low + high) // 2
        if key(items[middle]) < target:
            low = middle + 1
        else:
            high = middle
    return low


def find_anomalies(expenses, k=2):
    """Траты больше, чем среднее + k стандартных отклонений. Сложность: O(n)."""
    amounts = [e["amount"] for e in expenses]
    mean = sum(amounts) / len(amounts)
    variance = sum((a - mean) ** 2 for a in amounts) / len(amounts)
    threshold = mean + k * variance ** 0.5
    return [e for e in expenses if e["amount"] > threshold], threshold
