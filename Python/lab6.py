import random
import string
import unittest

def generate_password(length):
    if length <= 0:
        raise ValueError("Довжина пароля повинна бути позитивним числом.")
    
    # Список можливих символів (без цифр)
    all_characters = string.ascii_letters + string.punctuation
    
    # Переконуємось, що в паролі буде хоча б одна цифра
    password = [random.choice(string.digits)]  # Додаємо одну цифру
    
    # Генерація решти пароля
    password += [random.choice(all_characters) for _ in range(length - 1)]
    
    # Перемішуємо символи пароля, щоб цифра була випадковим чином
    random.shuffle(password)
    
    # Повертаємо пароль як рядок
    return ''.join(password)

class TestPasswordGeneration(unittest.TestCase):

    def test_password_length(self):
        length = 12
        password = generate_password(length)
        self.assertEqual(len(password), length, "Пароль має бути заданої довжини.")

    def test_password_content(self):
        length = 12
        password = generate_password(length)
        # Перевірка наявності великих і маленьких літер, цифр та спеціальних символів
        self.assertTrue(any(c.islower() for c in password), "Пароль повинен містити маленькі літери.")
        self.assertTrue(any(c.isupper() for c in password), "Пароль повинен містити великі літери.")
        self.assertTrue(any(c.isdigit() for c in password), "Пароль повинен містити цифри.")
        self.assertTrue(any(c in string.punctuation for c in password), "Пароль повинен містити спеціальні символи.")

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            generate_password(0)  # Тест на нульову довжину
        with self.assertRaises(ValueError):
            generate_password(-5)  # Тест на негативну довжину

if __name__ == "__main__":
    # Запуск тестів
    unittest.main()
