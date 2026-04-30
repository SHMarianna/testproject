import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_expenses():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)

def add_expense():
    amount = amount_entry.get().strip()
    category = category_entry.get().strip()
    date = date_entry.get().strip()

    if not amount or not category or not date:
        messagebox.showwarning("Ошибка", "Заполните все поля!")
        return

    try:
        amount_val = float(amount)
        if amount_val <= 0:
            messagebox.showwarning("Ошибка", "Сумма должна быть положительным числом!")
            return
    except:
        messagebox.showwarning("Ошибка", "Сумма должна быть числом!")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        messagebox.showwarning("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД (например, 2025-04-30)!")
        return

    expenses.append({"amount": amount_val, "category": category, "date": date})
    save_expenses()
    update_table()
    clear_entries()
    messagebox.showinfo("Успех", f"Расход {amount_val} руб добавлен!")

def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите запись для удаления!")
        return
    for item in selected:
        values = tree.item(item, "values")
        amount = float(values[0])
        category = values[1]
        date = values[2]
        for i, e in enumerate(expenses):
            if e["amount"] == amount and e["category"] == category and e["date"] == date:
                expenses.pop(i)
                break
    save_expenses()
    update_table()

def clear_entries():
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

def update_table(filtered_expenses=None):
    for row in tree.get_children():
        tree.delete(row)
    data = filtered_expenses if filtered_expenses is not None else expenses
    total = 0
    for e in data:
        tree.insert("", tk.END, values=(e["amount"], e["category"], e["date"]))
        total += e["amount"]
    total_label.config(text=f"Общая сумма: {total:.2f} руб")

def filter_by_category():
    category = category_filter_entry.get().strip()
    if not category:
        update_table()
        return
    filtered = [e for e in expenses if e["category"].lower() == category.lower()]
    update_table(filtered)

def filter_by_date():
    date = date_filter_entry.get().strip()
    if not date:
        update_table()
        return
    filtered = [e for e in expenses if e["date"] == date]
    update_table(filtered)

def filter_by_period():
    start = start_date_entry.get().strip()
    end = end_date_entry.get().strip()
    if not start or not end:
        messagebox.showwarning("Ошибка", "Введите обе даты!")
        return
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
    except:
        messagebox.showwarning("Ошибка", "Даты должны быть в формате ГГГГ-ММ-ДД!")
        return
    filtered = []
    for e in expenses:
        try:
            e_date = datetime.strptime(e["date"], "%Y-%m-%d")
            if start_date <= e_date <= end_date:
                filtered.append(e)
        except:
            continue
    update_table(filtered)
    total_period = sum(e["amount"] for e in filtered)
    messagebox.showinfo("Сумма за период", f"Расходы с {start} по {end}: {total_period:.2f} руб")

def reset_filters():
    category_filter_entry.delete(0, tk.END)
    date_filter_entry.delete(0, tk.END)
    start_date_entry.delete(0, tk.END)
    end_date_entry.delete(0, tk.END)
    update_table()

expenses = load_expenses()

window = tk.Tk()
window.title("Expense Tracker")
window.geometry("900x600")

input_frame = tk.LabelFrame(window, text="Добавление расхода", padx=10, pady=10)
input_frame.pack(fill="x", padx=10, pady=5)

tk.Label(input_frame, text="Сумма (руб):").grid(row=0, column=0, sticky="w")
amount_entry = tk.Entry(input_frame, width=15)
amount_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Категория:").grid(row=0, column=2, sticky="w")
category_entry = tk.Entry(input_frame, width=20)
category_entry.grid(row=0, column=3, padx=5)

tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, sticky="w")
date_entry = tk.Entry(input_frame, width=12)
date_entry.grid(row=0, column=5, padx=5)

btn_frame = tk.Frame(input_frame)
btn_frame.grid(row=1, column=0, columnspan=6, pady=10)
tk.Button(btn_frame, text="Добавить расход", command=add_expense, bg="green", fg="white").pack(side="left", padx=5)
tk.Button(btn_frame, text="Удалить выбранный", command=delete_expense, bg="red", fg="white").pack(side="left", padx=5)

filter_frame = tk.LabelFrame(window, text="Фильтрация", padx=10, pady=10)
filter_frame.pack(fill="x", padx=10, pady=5)

tk.Label(filter_frame, text="По категории:").grid(row=0, column=0)
category_filter_entry = tk.Entry(filter_frame, width=15)
category_filter_entry.grid(row=0, column=1, padx=5)
tk.Button(filter_frame, text="Применить", command=filter_by_category).grid(row=0, column=2, padx=5)

tk.Label(filter_frame, text="По дате (ГГГГ-ММ-ДД):").grid(row=0, column=3)
date_filter_entry = tk.Entry(filter_frame, width=12)
date_filter_entry.grid(row=0, column=4, padx=5)
tk.Button(filter_frame, text="Применить", command=filter_by_date).grid(row=0, column=5, padx=5)

tk.Label(filter_frame, text="Период с:").grid(row=1, column=0)
start_date_entry = tk.Entry(filter_frame, width=12)
start_date_entry.grid(row=1, column=1, padx=5)
tk.Label(filter_frame, text="по:").grid(row=1, column=2)
end_date_entry = tk.Entry(filter_frame, width=12)
end_date_entry.grid(row=1, column=3, padx=5)
tk.Button(filter_frame, text="Подсчитать сумму", command=filter_by_period, bg="orange").grid(row=1, column=4, padx=5)
tk.Button(filter_frame, text="Сбросить фильтры", command=reset_filters, bg="gray", fg="white").grid(row=1, column=5, padx=5)

tree_frame = tk.LabelFrame(window, text="Список расходов", padx=10, pady=10)
tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("Сумма", "Категория", "Дата")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill="both", expand=True)

total_label = tk.Label(window, text="Общая сумма: 0.00 руб", font=("Arial", 12, "bold"), fg="blue")
total_label.pack(pady=10)

update_table()
window.mainloop()