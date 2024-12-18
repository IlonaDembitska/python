from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Налаштування Selenium WebDriver
driver = webdriver.Chrome()  # Якщо потрібно, вказати шлях до драйвера

def scrape_instagram_hashtags(hashtag, num_posts=100):
    driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
    time.sleep(2)

    # Прокручування сторінки для завантаження постів
    for _ in range(num_posts // 10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # Збір хештегів з постів
    posts = driver.find_elements_by_xpath("//a[contains(@href, '/p/')]")
    hashtags = []
    for post in posts:
        post.click()
        time.sleep(2)

        try:
            # Збираємо хештеги з кожного поста
            caption = driver.find_element_by_xpath("//div[@class='_a9z6']")
            hashtags.extend([word for word in caption.text.split() if word.startswith('#')])
        except:
            continue

        driver.back()
        time.sleep(1)

    return hashtags

# Приклад використання
hashtag_data = scrape_instagram_hashtags('travel', 50)
driver.quit()

from collections import Counter

# Підрахунок частоти хештегів
hashtag_counts = Counter(hashtag_data)

# Перетворюємо в DataFrame для кращої обробки
df = pd.DataFrame(hashtag_counts.items(), columns=['Hashtag', 'Count'])
df = df.sort_values(by='Count', ascending=False)

# Виводимо топ 10 хештегів
print(df.head(10))


import matplotlib.pyplot as plt

# Створення графіка для топ-10 хештегів
plt.figure(figsize=(10, 6))
plt.barh(df['Hashtag'][:10], df['Count'][:10], color='skyblue')
plt.xlabel('Number of Mentions')
plt.ylabel('Hashtags')
plt.title('Top 10 Most Popular Hashtags')
plt.gca().invert_yaxis()  # Для правильного відображення
plt.show()



