import selenium

from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CappaRegAuth:
    """Класс для регистрации\\авторизации пользователя на сайте cappa.csu.ru"""
    def __init__(self, login:str, password:str, email:str, name:str, surname:str ):
        self.url = "https://cappa.csu.ru/"
        self.login = login
        self.password = password
        self.email = email
        self.name = name
        self.surname = surname

        self.options = EdgeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument('--disable-application-cache')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("--disable-setuid-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--headless")

    def registrate(self):
        try:
            with Edge(options=self.options) as driver:
                driver.get(self.url)
                # Дополнительный код для регистрации пользователя
                pass
        except Exception as e:
            print(f"Ошибка при регистрации: {e}")
            # Дополнительная обработка ошибок

    def authorizate(self):
        try:
            with Edge(options=self.options) as driver:
                driver.get(self.url)
                # Дополнительный код для авторизации пользователя
                pass
        except Exception as e:
            print(f"Ошибка при авторизации: {e}")
            # Дополнительная обработка ошибок
