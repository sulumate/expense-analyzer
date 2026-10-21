import csv
import os

import matplotlib.pyplot as plt
import pandas as pd

from algorithms import binary_search_first, categorize, find_anomalies, merge_sort

DATA_PATH = "data/expenses.csv"
OUTPUT_DIR = "output"


def load_expenses(path):
    """Читает CSV в список словарей и сразу проставляет категорию."""
    with open(path, encoding="utf-8") as f:
        expenses = list(csv.DictReader(f))
    for e in expenses:
        e["amount"] = int(e["amount"])
        e["category"] = categorize(e["description"])
    return expenses


def expenses_between(sorted_expenses, start, end):
    """Все траты с датой в [start, end] через два бинарных поиска."""
    by_date = lambda e: e["date"]
    left = binary_search_first(sorted_expenses, start, by_date)
    right = binary_search_first(sorted_expenses, end + "~", by_date)
    return sorted_expenses[left:right]


def make_charts(df):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    by_category = df.groupby("category")["amount"].sum().sort_values()
    by_category.plot(kind="barh", title="Расходы по категориям, ₸")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/by_category.png")
    plt.close()

    by_month = df.groupby(df["date"].dt.to_period("M"))["amount"].sum()
    by_month.plot(kind="line", marker="o", title="Расходы по месяцам, ₸")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/by_month.png")
    plt.close()


def main():
    expenses = load_expenses(DATA_PATH)
    print(f"Загружено трат: {len(expenses)}\n")

    sorted_expenses = merge_sort(expenses, key=lambda e: e["date"])
    print(f"Период: {sorted_expenses[0]['date']} — {sorted_expenses[-1]['date']}")

    september = expenses_between(sorted_expenses, "2026-09-01", "2026-09-30")
    print(f"Трат в сентябре: {len(september)} на сумму {sum(e['amount'] for e in september)} ₸\n")

    anomalies, threshold = find_anomalies(expenses)
    print(f"Необычно большие траты (больше {threshold:.0f} ₸):")
    for e in anomalies:
        print(f"  {e['date']}  {e['description']:<25} {e['amount']} ₸")

    df = pd.DataFrame(expenses)
    df["date"] = pd.to_datetime(df["date"])
    print("\nСумма по категориям:")
    print(df.groupby("category")["amount"].agg(["count", "sum", "mean"]).round(0)
          .sort_values("sum", ascending=False))

    make_charts(df)
    print(f"\nГрафики сохранены в папку {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
