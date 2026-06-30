import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class CalorieTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calorie Tracker для диабетиков")
        self.geometry("880x580")
        self.resizable(False, False)
        self.configure(padx=14, pady=14)
        self.create_widgets()

    def create_widgets(self):
        header = ttk.Label(
            self,
            text="Приложение для подсчёта калорий и контроля углеводов",
            font=("Segoe UI", 14, "bold"),
        )
        header.pack(anchor="w", pady=(0, 12))

        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", pady=(0, 8))

        labels = ["Блюдо", "Калории", "Углеводы (г)", "Сахар (г)", "Белки (г)"]
        self.entry_vars = [tk.StringVar() for _ in labels]
        self.insulin_ratio_var = tk.StringVar(value="10")

        for index, text in enumerate(labels):
            label = ttk.Label(input_frame, text=text)
            label.grid(row=0, column=index, padx=4, sticky="w")

        self.entries = []
        for index, width in enumerate((22, 10, 10, 10, 10)):
            entry = ttk.Entry(input_frame, textvariable=self.entry_vars[index], width=width)
            entry.grid(row=1, column=index, padx=4, sticky="w")
            self.entries.append(entry)

        ratio_label = ttk.Label(input_frame, text="Соотношение угл./инсулин")
        ratio_label.grid(row=0, column=5, padx=4, sticky="w")
        ratio_entry = ttk.Entry(input_frame, textvariable=self.insulin_ratio_var, width=12)
        ratio_entry.grid(row=1, column=5, padx=4, sticky="w")

        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill="x", pady=(0, 14))

        add_button = ttk.Button(buttons_frame, text="Добавить", command=self.add_item)
        add_button.pack(side="left", padx=(0, 6))

        remove_button = ttk.Button(buttons_frame, text="Удалить выбранное", command=self.remove_item)
        remove_button.pack(side="left", padx=(0, 6))

        clear_button = ttk.Button(buttons_frame, text="Очистить всё", command=self.clear_items)
        clear_button.pack(side="left", padx=(0, 6))

        save_button = ttk.Button(buttons_frame, text="Сохранить", command=self.save_items)
        save_button.pack(side="left", padx=(0, 6))

        load_button = ttk.Button(buttons_frame, text="Загрузить", command=self.load_items)
        load_button.pack(side="left")

        self.tree = ttk.Treeview(
            self,
            columns=("food", "calories", "carbs", "sugar", "protein"),
            show="headings",
            selectmode="browse",
            height=14,
        )
        self.tree.heading("food", text="Блюдо")
        self.tree.heading("calories", text="Калории")
        self.tree.heading("carbs", text="Углеводы")
        self.tree.heading("sugar", text="Сахар")
        self.tree.heading("protein", text="Белки")
        self.tree.column("food", width=210, anchor="w")
        self.tree.column("calories", width=110, anchor="center")
        self.tree.column("carbs", width=110, anchor="center")
        self.tree.column("sugar", width=110, anchor="center")
        self.tree.column("protein", width=110, anchor="center")
        self.tree.pack(fill="both", pady=(0, 12))

        total_frame = ttk.Frame(self)
        total_frame.pack(fill="x")

        self.total_calories_var = tk.StringVar(value="0")
        self.total_carbs_var = tk.StringVar(value="0")
        self.total_sugar_var = tk.StringVar(value="0")
        self.total_bread_units_var = tk.StringVar(value="0.00")
        self.insulin_units_var = tk.StringVar(value="0.00")

        stats = [
            ("Всего калорий:", self.total_calories_var),
            ("Всего углеводов:", self.total_carbs_var),
            ("Всего сахара:", self.total_sugar_var),
            ("Хлебные единицы:", self.total_bread_units_var),
            ("Оц. инсул. ед:", self.insulin_units_var),
        ]

        for text, var in stats:
            block = ttk.Frame(total_frame)
            block.pack(side="left", padx=10)
            label = ttk.Label(block, text=text)
            label.pack(anchor="w")
            value = ttk.Label(block, textvariable=var, font=("Segoe UI", 12, "bold"))
            value.pack(anchor="w")

        info_text = (
            "Контроль калорий, углеводов и сахара помогает диабетикам планировать питание и дозы инсулина. "
            "Хлебная единица рассчитывается как 12 г углеводов."
        )
        info_label = ttk.Label(self, text=info_text, wraplength=840, foreground="#333333")
        info_label.pack(fill="x", pady=(12, 0))

    def add_item(self):
        food = self.entry_vars[0].get().strip()
        calories_text = self.entry_vars[1].get().strip()
        carbs_text = self.entry_vars[2].get().strip()
        sugar_text = self.entry_vars[3].get().strip()
        protein_text = self.entry_vars[4].get().strip()

        if not food:
            messagebox.showwarning("Ошибка ввода", "Введите название блюда.")
            return

        try:
            calories = int(calories_text)
            carbs = float(carbs_text)
            sugar = float(sugar_text)
            protein = float(protein_text)
        except ValueError:
            messagebox.showwarning(
                "Ошибка ввода",
                "Пожалуйста, введите корректные числовые значения для калорий, углеводов, сахара и белков.",
            )
            return

        if calories < 0 or carbs < 0 or sugar < 0 or protein < 0:
            messagebox.showwarning("Ошибка ввода", "Значения должны быть неотрицательными.")
            return

        self.tree.insert("", "end", values=(food, calories, carbs, sugar, protein))
        self.clear_inputs()
        self.update_totals()

    def remove_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Удаление", "Выберите строку для удаления.")
            return
        for item in selected:
            self.tree.delete(item)
        self.update_totals()

    def clear_items(self):
        self.tree.delete(*self.tree.get_children())
        self.update_totals()

    def save_items(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Сохранить данные",
        )
        if not path:
            return

        try:
            items = [self.tree.item(item, "values") for item in self.tree.get_children()]
            data = {
                "items": [
                    {
                        "food": values[0],
                        "calories": int(values[1]),
                        "carbs": float(values[2]),
                        "sugar": float(values[3]),
                        "protein": float(values[4]),
                    }
                    for values in items
                ],
                "insulin_ratio": self.insulin_ratio_var.get(),
            }
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            messagebox.showinfo("Сохранение", "Данные успешно сохранены.")
        except Exception as exc:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {exc}")

    def load_items(self):
        path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Загрузить данные",
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.tree.delete(*self.tree.get_children())
            for item in data.get("items", []):
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        item.get("food", ""),
                        int(item.get("calories", 0)),
                        float(item.get("carbs", 0.0)),
                        float(item.get("sugar", 0.0)),
                        float(item.get("protein", 0.0)),
                    ),
                )
            self.insulin_ratio_var.set(str(data.get("insulin_ratio", "10")))
            self.update_totals()
            messagebox.showinfo("Загрузка", "Данные успешно загружены.")
        except Exception as exc:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {exc}")

    def clear_inputs(self):
        for var in self.entry_vars:
            var.set("")
        self.entries[0].focus()

    def update_totals(self):
        total_calories = 0
        total_carbs = 0.0
        total_sugar = 0.0

        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            try:
                total_calories += int(values[1])
                total_carbs += float(values[2])
                total_sugar += float(values[3])
            except (ValueError, TypeError, IndexError):
                continue

        self.total_calories_var.set(str(total_calories))
        self.total_carbs_var.set(f"{total_carbs:.1f}")
        self.total_sugar_var.set(f"{total_sugar:.1f}")
        self.total_bread_units_var.set(f"{self.calculate_bread_units(total_carbs):.2f}")
        self.insulin_units_var.set(self.estimate_insulin_units(total_carbs))

    def calculate_bread_units(self, carbs):
        return carbs / 12.0 if carbs >= 0 else 0.0

    def estimate_insulin_units(self, carbs):
        try:
            ratio = float(self.insulin_ratio_var.get())
            if ratio <= 0:
                return "N/A"
            return f"{carbs / ratio:.2f}"
        except ValueError:
            return "N/A"


if __name__ == "__main__":
    app = CalorieTrackerApp()
    app.mainloop()
