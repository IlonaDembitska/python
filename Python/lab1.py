# Імпортуємо необхідні бібліотеки
from dataclasses import dataclass
from typing import List, Optional
import json

# Клас Book описує окрему книгу
@dataclass
class Book:
    title: str  # Назва книги
    author: str  # Автор книги
    year: int  # Рік видання
    genre: str  # Жанр книги

    # Метод для перевірки правильності року видання
    def __post_init__(self):
        if not isinstance(self.year, int) or self.year <= 0:
            raise ValueError(f"Рік видання має бути позитивним цілим числом, отримано: {self.year}")

    # Перетворюємо книгу в словник для збереження у файл
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre
        }

    # Створюємо книгу зі словника, наприклад, при завантаженні з файлу
    @staticmethod
    def from_dict(data):
        return Book(
            title=data["title"],
            author=data["author"],
            year=data["year"],
            genre=data["genre"]
        )

# Клас Library для роботи з бібліотекою
class Library:
    def __init__(self):
        # Список для зберігання книг
        self.books: List[Book] = []

    # Додаємо книгу до бібліотеки
    def add_book(self, book: Book):
        if self._find_book(book.title, book.author):
            print(f"Книга '{book.title}' автора '{book.author}' вже існує в бібліотеці.")
            return
        self.books.append(book)
        print(f"Додано книгу: {book.title} автор {book.author}.")

    # Видаляємо книгу з бібліотеки
    def remove_book(self, title: str, author: str):
        book = self._find_book(title, author)
        if book:
            self.books.remove(book)
            print(f"Видалено книгу: {book.title} автора {book.author}.")
        else:
            print(f"Книга '{title}' автора '{author}' не знайдена в бібліотеці.")

    # Шукаємо книги за автором
    def search_by_author(self, author: str) -> List[Book]:
        found_books = [book for book in self.books if book.author.lower() == author.lower()]
        print(f"Знайдено {len(found_books)} книг автора '{author}'.")
        return found_books

    # Шукаємо книги за жанром
    def search_by_genre(self, genre: str) -> List[Book]:
        found_books = [book for book in self.books if book.genre.lower() == genre.lower()]
        print(f"Знайдено {len(found_books)} книг жанру '{genre}'.")
        return found_books

    # Виводимо список усіх книг із можливістю сортування
    def list_books(self, sort_by: Optional[str] = None) -> List[Book]:
        if sort_by == "year":
            sorted_books = sorted(self.books, key=lambda book: book.year)
            print("Список книг відсортовано за роком видання.")
        elif sort_by == "title":
            sorted_books = sorted(self.books, key=lambda book: book.title.lower())
            print("Список книг відсортовано за назвою.")
        else:
            sorted_books = self.books
            print("Список книг без сортування.")
        return sorted_books

    # Зберігаємо бібліотеку у файл
    def save_to_file(self, filename: str):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)
            print(f"Бібліотека збережена у файл '{filename}'.")
        except Exception as e:
            print(f"Помилка при збереженні бібліотеки: {e}")

    # Завантажуємо бібліотеку з файлу
    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                books_data = json.load(f)
                self.books = [Book.from_dict(book) for book in books_data]
            print(f"Бібліотека завантажена з файлу '{filename}'.")
        except FileNotFoundError:
            print(f"Файл '{filename}' не знайдено.")
        except json.JSONDecodeError:
            print(f"Файл '{filename}' має неправильний формат.")
        except Exception as e:
            print(f"Помилка при завантаженні бібліотеки: {e}")

    # Приватний метод для пошуку книги
    def _find_book(self, title: str, author: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower() and book.author.lower() == author.lower():
                return book
        return None

# Основна частина програми (демонстрація)
if __name__ == "__main__":
    # Створюємо бібліотеку
    library = Library()

    # Додаємо книги
    book1 = Book(title="1984", author="Джордж Орвелл", year=1949, genre="Дистопія")
    book2 = Book(title="To Kill a Mockingbird", author="Harper Lee", year=1960, genre="Класика")
    book3 = Book(title="The Great Gatsby", author="F. Scott Fitzgerald", year=1925, genre="Класика")
    book4 = Book(title="Brave New World", author="Aldous Huxley", year=1932, genre="Дистопія")

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    library.add_book(book4)

    # Видаляємо книгу
    library.remove_book("1984", "Джордж Орвелл")

    # Пошук за автором
    classics = library.search_by_author("Harper Lee")
    for book in classics:
        print(book)

    # Пошук за жанром
    dystopian = library.search_by_genre("Дистопія")
    for book in dystopian:
        print(book)

    # Сортуємо та виводимо книги
    sorted_by_year = library.list_books(sort_by="year")
    for book in sorted_by_year:
        print(book)

    # Зберігаємо бібліотеку у файл
    library.save_to_file("library.json")

    # Завантажуємо бібліотеку з файлу
    new_library = Library()
    new_library.load_from_file("library.json")
    for book in new_library.list_books():
        print(book)
