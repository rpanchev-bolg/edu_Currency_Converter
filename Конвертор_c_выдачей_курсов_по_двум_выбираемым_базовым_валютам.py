from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests


def update_currency_label(event):
    # Получаем полное название валюты из словаря и обновляем метку
    match event.widget.winfo_name():
        case 'base_label':
            code = base_combobox.get()
            if code == base2_combobox.get():
                mb.showwarning("Внимание", f"Валюта {code} уже выбрана в качестве второй базовой!!!")
                base_combobox.set("")
            else:
                name = currencies[code]
                b_label.config(text=name)
        case 'base2_label':
            code = base2_combobox.get()
            if code == base_combobox.get():
                mb.showwarning("Внимание", f"Валюта {code} уже выбрана в качестве первой базовой!!!")
                base2_combobox.set("")
            else:
                name = currencies[code]
                b2_label.config(text=name)
        case 'target_label':
            code = target_combobox.get()
            name = currencies[code]
            t_label.config(text=name)

def get_exchange_rates(base, target):
    try:
        response = requests.get(f'https://open.er-api.com/v6/latest/'
                                f'{base}')
        response.raise_for_status()
        data = response.json()
        if target in data['rates']:
            return data['rates'][target]
        else:
            mb.showerror("Ошибка", f"Валюта {target} не найдена")
            return None
    except Exception as e:
        mb.showerror("Ошибка", f"Ошибка: {e}")
        return None

def exchange():
    target_code = target_combobox.get()
    base_code = base_combobox.get()
    if target_code and base_code:
        exchange_rate1 = get_exchange_rates(base_code, target_code)
    else:
        mb.showwarning("Внимание", "Выберите коды валют")
        return

    base2_code = base2_combobox.get()
    exchange_rate2 = None
    if target_code and base2_code:
        exchange_rate2 = get_exchange_rates(base2_code, target_code)

    msg = ''
    target = currencies[target_code]
    if exchange_rate1:
        base = currencies[base_code]
        msg = (f"Курс1: {exchange_rate1:.2f} {target}"
               f"\nза 1 {base}")

    if exchange_rate1 and exchange_rate2:
        base = currencies[base2_code]
        msg += (f"\n\nКурс2: {exchange_rate2:.2f} {target}"
               f"\nза 1 {base}")
    if msg:
        mb.showinfo("Курс обмена", msg)
    else:
        mb.showwarning("Внимание", "Курсы валют не удалось получить!!!")


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
window.geometry("340x300")

Label(text="Базовая валюта:   ", font='Courier 9').pack(padx=10, pady=(10, 2))
base_combobox = ttk.Combobox(width=16, values=list(currencies.keys()),
                             name='base_label')
base_combobox.pack(padx=10, pady=(0, 5))
base_combobox.bind("<<ComboboxSelected>>", update_currency_label)

b_label = ttk.Label()
b_label.pack(padx=10, pady=(0,5))

Label(text="Вторая базовая валюта:", font='Courier 9').pack(padx=10, pady=(5, 2))
base2_combobox = ttk.Combobox(width=16, values=list(currencies.keys()),
                             name='base2_label')
base2_combobox.pack(padx=10, pady=(0, 5))
base2_combobox.bind("<<ComboboxSelected>>", update_currency_label)

b2_label = ttk.Label()
b2_label.pack(padx=10, pady=(0,10))

Label(text="Целевая валюта:   ", font='Courier 9').pack(padx=10, pady=(10, 2))
target_combobox = ttk.Combobox(width=16, values=list(currencies.keys()),
                               name='target_label')
target_combobox.pack(padx=10, pady=(0, 5))
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=(0, 5))

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)

window.mainloop()
