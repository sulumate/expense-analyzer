"""Генерирует тестовый файл data/expenses.csv со случайными тратами."""
import csv
import os
import random
from datetime import date, timedelta

DESCRIPTIONS = {
    "Magnum супермаркет": (3000, 25000),
    "Small продукты": (1000, 8000),
    "Яндекс Такси": (800, 4000),
    "Автобус Onay": (100, 300),
    "Starbucks кофе": (1500, 3500),
    "KFC обед": (2500, 6000),
    "Kaspi Netflix подписка": (2500, 2500),
    "Spotify подписка": (1500, 1500),
    "Аптека": (1000, 10000),
    "Kino.kz билеты": (2500, 6000),
    "Zara одежда": (10000, 40000),
    "Коммунальные услуги": (15000, 30000),
}


def generate(rows=200, seed=42):
    random.seed(seed)
    start = date(2026, 7, 1)
    expenses = []
    for _ in range(rows):
        description = random.choice(list(DESCRIPTIONS))
        low, high = DESCRIPTIONS[description]
        amount = random.randint(low, high)
        day = start + timedelta(days=random.randint(0, 109))
        expenses.append([day.isoformat(), description, amount])

    expenses.append(["2026-09-14", "Zara одежда", 150000])
    expenses.append(["2026-10-02", "Magnum супермаркет", 120000])

    random.shuffle(expenses)
    return expenses


def save(expenses, path="data/expenses.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "description", "amount"])
        writer.writerows(expenses)
    print(f"Сохранено {len(expenses)} строк в {path}")


if __name__ == "__main__":
    save(generate())
