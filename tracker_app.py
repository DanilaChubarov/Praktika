import ctypes
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from storage import (
    calculate_bread_units,
    calculate_totals,
    estimate_insulin_units,
    load_data,
    save_data,
)


class CalorieTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self._configure_high_dpi()
        self.title("Calorie Tracker для диабетиков")
        self.geometry("920x600")
        self.resizable(False, False)
        self.configure(padx=16, pady=16, bg="#f1f4f8")

        self.entry_vars = []
        self.insulin_ratio_var = tk.StringVar(master=self, value="10")
        self.total_calories_var = tk.StringVar(master=self, value="0")
        self.total_carbs_var = tk.StringVar(master=self, value="0")
        self.total_sugar_var = tk.StringVar(master=self, value="0")
        self.total_bread_units_var = tk.StringVar(master=self, value="0.00")
        self.insulin_units_var = tk.StringVar(master=self, value="0.00")

        self._create_style()
        self._create_widgets()

    def _configure_high_dpi(self):
        if sys.platform == "win32":
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except Exception:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass
        try:
            self.tk.call("tk", "scaling", 1.0)
        except Exception:
            pass

    def _create_style(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure(
            ".",
            background="#f1f4f8",
            foreground="#202124",
            font=("Segoe UI", 10),
        )
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1f4e79")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 10, "bold"))
        self.style.configure("StatValue.TLabel", font=("Segoe UI", 12, "bold"), foreground="#0f4c75")
        self.style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(10, 6))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        self.style.map(
            "Accent.TButton",
            background=[("active", "#3f72af"), ("!active", "#4f6fad")],
            foreground=[("!disabled", "white")],
        )

    def _create_widgets(self):
        title_label = ttk.Label(
            self,
            text="Контроль калорий и углеводов для диабетиков",
            style="Header.TLabel",
        )
        title_label.pack(anchor="w", pady=(0, 16))

        input_frame = ttk.Frame(self, padding=12, style="Card.TFrame")
        input_frame.pack(fill="x", pady=(0, 16))

        labels = ["Блюдо", "Калории", "Углеводы (г)", "Сахар (г)", "Белки (г)"]
        self.entry_vars = [tk.StringVar(master=self) for _ in labels]

        for index, text in enumerate(labels):
            label = ttk.Label(input_frame, text=text, style="SubHeader.TLabel")
            label.grid(row=0, column=index, padx=6, pady=(0, 6), sticky="w")

        self.entries = []
        widths = (24, 10, 10, 10, 10)
        for index, width in enumerate(widths):
            entry = ttk.Entry(input_frame, textvariable=self.entry_vars[index], width=width)
            entry.grid(row=1, column=index, padx=6, sticky="w")
            self.entries.append(entry)

        insulin_label = ttk.Label(input_frame, text="Соотношение угл./инсулин", style="SubHeader.TLabel")
        insulin_label.grid(row=0, column=5, padx=6, sticky="w")
        insulin_entry = ttk.Entry(input_frame, textvariable=self.insulin_ratio_var, width=12)
        insulin_entry.grid(row=1, column=5, padx=6, sticky="w")

        button_frame = ttk.Frame(self, padding=4)
        button_frame.pack(fill="x", pady=(0, 16))

        actions = [
            ("Добавить", self.add_item),
            ("Удалить выбранное", self.remove_item),
            ("Очистить всё", self.clear_items),
            ("Сохранить", self.save_items),
            ("Загрузить", self.load_items),
        ]

        for text, command in actions:
            button = ttk.Button(button_frame, text=text, command=command, style="Accent.TButton")
            button.pack(side="left", padx=6, ipadx=4)

        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill="both", expand=True)

        columns = ("food", "calories", "carbs", "sugar", "protein")
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=14,
            style="Custom.Treeview",
        )
        self.tree.heading("food", text="Блюдо")
        self.tree.heading("calories", text="Калории")
        self.tree.heading("carbs", text="Углеводы")
        self.tree.heading("sugar", text="Сахар")
        self.tree.heading("protein", text="Белки")
        self.tree.column("food", width=260, anchor="w")
        self.tree.column("calories", width=110, anchor="center")
        self.tree.column("carbs", width=110, anchor="center")
        self.tree.column("sugar", width=110, anchor="center")
        self.tree.column("protein", width=110, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill="x", pady=14)

        total_frame = ttk.Frame(self, padding=12, style="Card.TFrame")
        total_frame.pack(fill="x")

        stat_items = [
            ("Всего калорий", self.total_calories_var),
            ("Всего углеводов", self.total_carbs_var),
            ("Всего сахара", self.total_sugar_var),
            ("Хлебные ед.", self.total_bread_units_var),
            ("Инсул. ед.", self.insulin_units_var),
        ]

        for text, var in stat_items:
            stat_block = ttk.Frame(total_frame)
            stat_block.pack(side="left", padx=12)
            label = ttk.Label(stat_block, text=text)
            label.pack(anchor="w")
            value = ttk.Label(stat_block, textvariable=var, style="StatValue.TLabel")
            value.pack(anchor="w")

        info_text = (
            "Управляйте углеводами и сахаром, чтобы планировать питание и дозы инсулина. "
            "Используйте функцию сохранения для хранения дневных меню."
        )
        info_label = ttk.Label(self, text=info_text, wraplength=880, foreground="#334155")
        info_label.pack(fill="x", pady=(14, 0))

    def _get_items(self):
        return [
            {
                "food": self.tree.item(item, "values")[0],
                "calories": self.tree.item(item, "values")[1],
                "carbs": self.tree.item(item, "values")[2],
                "sugar": self.tree.item(item, "values")[3],
                "protein": self.tree.item(item, "values")[4],
            }
            for item in self.tree.get_children()
        ]

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
            save_data(path, self._get_items(), self.insulin_ratio_var.get())
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
            data = load_data(path)
            self.tree.delete(*self.tree.get_children())
            for item in data["items"]:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        item["food"],
                        item["calories"],
                        item["carbs"],
                        item["sugar"],
                        item["protein"],
                    ),
                )
            self.insulin_ratio_var.set(data["insulin_ratio"])
            self.update_totals()
            messagebox.showinfo("Загрузка", "Данные успешно загружены.")
        except Exception as exc:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {exc}")

    def clear_inputs(self):
        for var in self.entry_vars:
            var.set("")
        self.entries[0].focus()

    def update_totals(self):
        items = self._get_items()
        totals = calculate_totals(items)
        insulin_ratio = 0.0
        try:
            insulin_ratio = float(self.insulin_ratio_var.get())
        except ValueError:
            insulin_ratio = 0.0

        self.total_calories_var.set(str(totals["calories"]))
        self.total_carbs_var.set(f"{totals['carbs']:.1f}")
        self.total_sugar_var.set(f"{totals['sugar']:.1f}")
        self.total_bread_units_var.set(f"{calculate_bread_units(totals['carbs']):.2f}")
        self.insulin_units_var.set(
            f"{estimate_insulin_units(totals['carbs'], insulin_ratio):.2f}"
            if insulin_ratio > 0
            else "N/A"
        )
