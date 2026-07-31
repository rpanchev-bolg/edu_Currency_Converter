from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests


def update_currency_label(event):
    # Получаем полное название валюты из словаря и обновляем метку
    match event.widget.winfo_name():
        case 'base_label':
            code = base_combobox.get()
            name = currencies[code]
            b_label.config(text=name)
        case 'target_label':
            code = target_combobox.get()
            name = currencies[code]
            t_label.config(text=name)


def exchange():
    target_code = target_combobox.get()
    base_code = base_combobox.get()

    if target_code and base_code:
        try:
            response = requests.get(f'https://open.er-api.com/v6/latest/'
                                    f'{base_code}')
            response.raise_for_status()
            data = response.json()
            if target_code in data['rates']:
                exchange_rate = data['rates'][target_code]
                base = currencies[base_code]
                target = currencies[target_code]
                mb.showinfo("Курс обмена", f"Курс {exchange_rate:.2f} {target}"
                                           f"\nза 1 {base}")
            else:
                mb.showerror("Ошибка", f"Валюта {target_code} не найдена")
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
    else:
        mb.showwarning("Внимание", "Выберите коды валют")


# Словарь кодов валют и их полных названий
currencies = {"USD": "Американский доллар", "EUR": "Евро",
              "JPY": "Японская йена", "GBP": "Британский фунт стерлингов",
              "AUD": "Австралийский доллар", "CAD": "Канадский доллар",
              "CHF": "Швейцарский франк", "CNY": "Китайский юань",
              "RUB": "Российский рубль", "KZT": "Казахстанский тенге",
              "UZS": "Узбекский сум"}
# Создание графического интерфейса
window = Tk()
window.title("Курс обмена валюты")
window.geometry("360x240")

Label(text="Базовая валюта:").pack(padx=10, pady=(10, 2))
base_combobox = ttk.Combobox(width=12, values=list(currencies.keys()),
                             name='base_label')
base_combobox.pack(padx=10, pady=(0, 5))
base_combobox.bind("<<ComboboxSelected>>", update_currency_label)

b_label = ttk.Label()
b_label.pack(padx=10, pady=(0,10))

Label(text="Целевая валюта:").pack(padx=10, pady=(10, 2))
target_combobox = ttk.Combobox(width=12, values=list(currencies.keys()),
                               name='target_label')
target_combobox.pack(padx=10, pady=(0, 5))
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=(0, 10))

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)

window.mainloop()
