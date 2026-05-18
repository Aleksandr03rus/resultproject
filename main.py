import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")

        # Переменные
        self.length = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        self.history = []

        self.load_history()
        self.setup_ui()

    def setup_ui(self):
        # Ползунок длины
        ttk.Label(self.root, text="Длина пароля:").pack(pady=5)
        length_scale = ttk.Scale(self.root, from_=4, to=64,
                                 variable=self.length, orient=tk.HORIZONTAL)
        length_scale.pack(pady=5, fill=tk.X, padx=20)
        self.length_label = ttk.Label(self.root, text=f"{self.length.get()}")
        self.length_label.pack()

        # Чекбоксы
        ttk.Checkbutton(self.root, text="Цифры (0-9)",
                        variable=self.use_digits).pack(anchor=tk.W, padx=20)
        ttk.Checkbutton(self.root, text="Буквы (A-Z, a-z)",
                        variable=self.use_letters).pack(anchor=tk.W, padx=20)
        ttk.Checkbutton(self.root, text="Спецсимволы (!@#$% и т.д.)",
                        variable=self.use_special).pack(anchor=tk.W, padx=20)

        # Кнопка генерации
        generate_btn = ttk.Button(self.root, text="Сгенерировать пароль",
                                  command=self.generate_password)
        generate_btn.pack(pady=10)

        # Поле вывода пароля
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(self.root, textvariable=self.password_var,
                               font=("Courier", 12), state="readonly")
        password_entry.pack(pady=5, fill=tk.X, padx=20)

        # Таблица истории
        ttk.Label(self.root, text="История паролей:").pack(pady=5)
        columns = ("ID", "Пароль", "Длина", "Символы")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=5, fill=tk.BOTH, padx=20, expand=True)

        # Обновление ползунка
        length_scale.config(command=self.update_length_label)

        # Загрузка истории в таблицу
        self.refresh_history_table()

    def update_length_label(self, value):
        self.length_label.config(text=f"{int(float(value))}")

    def generate_password(self):
        length = self.length.get()
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа")
            return
        if length > 64:
            messagebox.showerror("Ошибка", "Максимальная длина пароля — 64 символа")
            return

        chars = ""
        if self.use_digits.get():
            chars += "0123456789"
        if self.use_letters.get():
            chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        if self.use_special.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)

        # Добавление в историю
        symbols = "".join(["Ц" if self.use_digits.get() else "",
                          "Б" if self.use_letters.get() else "",
                          "С" if self.use_special.get() else ""])
        entry = {
            "id": len(self.history) + 1,
            "password": password,
            "length": length,
            "symbols": symbols
        }
        self.history.append(entry)
        self.save_history()
        self.refresh_history_table()

    def refresh_history_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.history:
            self.tree.insert("", tk.END, values=(
                entry["id"], entry["password"], entry["length"], entry["symbols"]
            ))

    def load_history(self):
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
