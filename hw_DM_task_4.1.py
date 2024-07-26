"""
1. Выберите веб-сайт с табличными данными, который вас интересует.
2. Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
3. Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
4. Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

Ваш код должен включать следующее:
1. Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
2. Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
3. Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
4. Комментарии для объяснения цели и логики кода.

Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.
"""

import requests
from lxml import html
import csv
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
            data.append([cell.text_content().strip() for cell in cells])

    # Сохранение данных в CSV-файл
    with open("countries_population.csv", "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)

        # Запись заголовков
        csvwriter.writerow(headers)

        # Запись строк данных
        csvwriter.writerows(data)

    print("Данные успешно сохранены в файл countries_population.csv")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении HTTP-запроса: {e}")
except ValueError as e:
    print(f"Ошибка обработки данных: {e}")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")
