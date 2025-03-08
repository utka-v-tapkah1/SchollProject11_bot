import asyncio
import logging
import os
from playwright.async_api import async_playwright


# Настройки
url = "https://foodmonitoring.ru/11679/food"
download_path = "./xlsx_downloads"  # Локальная папка для загрузки файлов

logger = logging.getLogger(__name__)


async def _wait_for_download():
    """Ожидает завершения загрузки файлов."""
    while True:
        files = os.listdir(download_path)
        tmp_files = [f for f in files if f.endswith('.tmp')]
        if not tmp_files:
            break
        await asyncio.sleep(0.1)


async def parse_xlsx(today):
    """Скачивает xlsx-файл за указанную дату."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Открытие сайта
            await page.goto(url)

            day = today.split('-')[2]

            # Ожидание появления кнопки
            button_selector = f"//a[contains(@class, '__btn-success') and normalize-space(text())={day}]"
            await page.wait_for_selector(button_selector, state="visible", timeout=1500)

            # Нажатие на кнопку
            button = page.locator(button_selector)
            await button.click()

            # Ожидание загрузки контента после нажатия кнопки
            await page.wait_for_selector("a[href$='.xlsx']", state="visible")

            # Поиск ссылок на xlsx-файлы
            links = await page.locator("a[href$='.xlsx']").all()
            xlsx_links = [await link.get_attribute("href") for link in links]

            # Фильтрация по дате
            if today in xlsx_links[0]:
                logger.info(f"Скачиваем файл: {xlsx_links[0]}")

                # Загрузка файла
                async with page.expect_download() as download_info:
                    await page.locator(f"a[href='{xlsx_links[0]}']").click()

                download = await download_info.value
                file_path = os.path.join(download_path, download.suggested_filename)
                await download.save_as(file_path)

                # Проверка загрузки
                logger.info(f"Файл успешно скачан: {file_path}")

        except Exception as e:
            logger.error(f"Ошибка: {e}")

        finally:
            # Закрыть браузер
            await browser.close()