import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from googletrans import Translator

# Імітовані дані
data = {
    'post': [
        "Це був чудовий день!",
        "Все погано, нічого не виходить...",
        "Я неймовірно щасливий!",
        "Нічого особливого",
        "Це катастрофа!",
        "Не знаю, що робити...",
        "Справжнє свято!"
    ],
    'likes': [120, 15, 200, 50, 10, 30, 180]
}

# Створення DataFrame з даних
df = pd.DataFrame(data)

# Виведення таблиці на екран
print("Таблиця даних:")
print(df)

# Функція для перекладу та визначення настрою поста
translator = Translator()

def get_sentiment(text):
    # Переклад тексту на англійську для аналізу
    translation = translator.translate(text, src='uk', dest='en')
    # Аналіз настрою
    analysis = TextBlob(translation.text)
    # Повертаємо настрій в залежності від полярності
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

# Додавання колонки з настроєм поста
df['sentiment'] = df['post'].apply(get_sentiment)

# Виведення таблиці з настроєм
print("\nТаблиця з визначеними настроями:")
print(df)

# Підрахунок лайків для кожного настрою
likes_by_sentiment = df.groupby('sentiment')['likes'].sum()

# Візуалізація результатів
plt.figure(figsize=(10, 6))
likes_by_sentiment.plot(kind='bar', color=['green', 'blue', 'red'])

# Налаштування графіка
plt.title('Залежність кількості лайків від настрою постів')
plt.xlabel('Настрій')
plt.ylabel('Кількість лайків')
plt.xticks(rotation=0)

# Показ графіка
plt.show()
