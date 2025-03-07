import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Настройки
url = "https://foodmonitoring.ru/11679/food"
download_path = "./xlsx_downloads"  # Локальная папка для загрузки файлов

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def _wait_for_download() -> None:
    while True:
        files = os.listdir(download_path)
        tmp_files = [f for f in files if f.endswith('.tmp')]
        if not tmp_files:
            break
        time.sleep(1)


def parse_xlsx(today):
    # Настройка Chrome WebDriver
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": os.path.abspath(download_path)}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Открытие сайта
        driver.get(url)

        day = today.split('-')[2]
        # Ожидание появления кнопки
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[contains(@class, '__btn-success') and normalize-space(text())={day}]"))
        )
        # Нажатие на кнопку
        button.click()

        # Ожидание загрузки контента после нажатия кнопки
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        # Поиск ссылок на xlsx-файлы
        links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '.xlsx')]"))
        )
        # links = driver.find_elements(By.TAG_NAME, "a")
        xlsx_link = [link.get_attribute("href") for link in links if
                     link.get_attribute("href") and ".xlsx" in link.get_attribute("href")]
        # Фильтрация по дате
        if today in xlsx_link[0]:
            # _delete_files_in_folder('./xlsx_downloads')
            print(f"Скачиваем файл: {xlsx_link}")
            driver.get(xlsx_link[0])  # Переход по ссылке, чтобы загрузить файл
            _wait_for_download()
            print('Загрузка завершена')

        files = os.listdir(download_path)
        xlsx_files = [f for f in files if f.endswith('.xlsx')]
        if xlsx_files:
            print(f"Файл успешно скачан: {xlsx_files[0]}")
        else:
            print("Не удалось найти скачанный файл.")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        # Закрыть браузер
        driver.quit()
