import tkinter as tk
import random

class CatchMeIfYouCan:
    def __init__(self, root):
        self.root = root
        self.root.title("Піймай мене, якщо зможеш")
        
        # Налаштування
        self.speed_settings = {"Легко": 300, "Середньо": 200, "Важко": 100}  # Швидкість втечі кнопки
        self.speed = self.speed_settings["Середньо"]
        self.attempts = 0
        self.is_game_over = False
        
        # Лейбли
        self.attempts_label = tk.Label(self.root, text="Спроби: 0")
        self.attempts_label.pack(pady=20)
        
        self.info_label = tk.Label(self.root, text="Натискайте на кнопку, щоб впіймати її!")
        self.info_label.pack(pady=20)
        
        # Кнопка, що втікає
        self.catch_button = tk.Button(self.root, text="Піймай мене!", command=self.catch_button_clicked)
        self.catch_button.pack(pady=50)

        # Кнопка для зміни швидкості
        self.speed_label = tk.Label(self.root, text="Виберіть складність:")
        self.speed_label.pack(pady=10)
        
        self.easy_button = tk.Button(self.root, text="Легко", command=lambda: self.set_speed("Легко"))
        self.easy_button.pack(side="left", padx=10)
        
        self.medium_button = tk.Button(self.root, text="Середньо", command=lambda: self.set_speed("Середньо"))
        self.medium_button.pack(side="left", padx=10)
        
        self.hard_button = tk.Button(self.root, text="Важко", command=lambda: self.set_speed("Важко"))
        self.hard_button.pack(side="left", padx=10)

        # Початкове встановлення розміру вікна
        self.root.geometry("500x400")  # Встановлюємо розмір вікна
        self.root.after(100, self.move_button)  # Переміщення кнопки після ініціалізації вікна

    def set_speed(self, level):
        """Змінюємо швидкість втечі кнопки"""
        self.speed = self.speed_settings[level]
        if not self.is_game_over:
            self.move_button()

    def move_button(self):
        """Переміщаємо кнопку в випадкову позицію"""
        if self.is_game_over:
            return
        
        # Переконатися, що розміри вікна вже доступні
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Генерація випадкових координат, щоб кнопка не виходила за межі вікна
        x = random.randint(50, width - 150)
        y = random.randint(50, height - 150)

        # Плавне переміщення кнопки
        self.catch_button.place(x=x, y=y)
        
        # Збільшуємо лічильник спроб
        self.attempts += 1
        self.attempts_label.config(text=f"Спроби: {self.attempts}")
        
        # Затримка для переміщення
        self.root.after(self.speed, self.move_button)

    def catch_button_clicked(self):
        """Коли користувач натискає на кнопку"""
        if self.is_game_over:
            return
        
        self.is_game_over = True
        self.info_label.config(text="Ти впіймав мене!")
        self.catch_button.config(text="Грати знову", command=self.restart_game)

    def restart_game(self):
        """Перезапуск гри"""
        self.is_game_over = False
        self.attempts = 0
        self.attempts_label.config(text="Спроби: 0")
        self.info_label.config(text="Натискайте на кнопку, щоб впіймати її!")
        self.catch_button.config(text="Піймай мене!")
        self.move_button()

if __name__ == "__main__":
    root = tk.Tk()
    game = CatchMeIfYouCan(root)
    root.mainloop()
