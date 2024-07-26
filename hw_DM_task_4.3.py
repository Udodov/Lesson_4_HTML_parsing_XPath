"""
- Парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
- Сохранение данных в базу данных MongoDB
"""

import requests
from lxml import html
import pymongo
import time

# URL страницы Wikipedia с таблицей
url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"

# Заголовок агента пользователя для имитации веб-браузера
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"
}

try:
    # Добавление задержки перед запросом
    time.sleep(2)  # Задержка в 2 секунды

    # Отправка GET-запроса к странице
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Проверка успешности запроса

    # Парсинг HTML содержимого страницы
    tree = html.fromstring(response.content)

    # XPath для нахождения таблицы на странице
    table_xpath = '//*[@id="mw-content-text"]/div[1]/table[1]'

    # Извлечение таблицы
    table = tree.xpath(table_xpath)

    if not table:
        raise ValueError("Таблица не найдена на странице.")

    table = table[0]

    # Извлечение строк таблицы
    rows = table.xpath(".//tr")

    # Парсинг заголовков таблицы
    headers = [header.text_content().strip() for header in rows[0].xpath(".//th")]

    # Парсинг данных таблицы
    data = []
    for row in rows[1:]:
        cells = row.xpath(".//td")
        if len(cells) > 0:
            data.append(
                {
                    headers[i]: cell.text_content().strip()
                    for i, cell in enumerate(cells)
                }
            )

    # Подключение к MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Создание базы данных и коллекции
    db = client["population_db"]
    collection = db["countries_population"]

    # Вставка данных в коллекцию
    collection.insert_many(data)

    print("Данные успешно сохранены в базу данных MongoDB")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении HTTP-запроса: {e}")
except ValueError as e:
    print(f"Ошибка обработки данных: {e}")
except pymongo.errors.PyMongoError as e:
    print(f"Ошибка при работе с MongoDB: {e}")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")
