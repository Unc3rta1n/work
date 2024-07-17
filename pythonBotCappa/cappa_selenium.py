import selenium

from undetected_chromedriver import Chrome, ChromeOptions
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
        
        self.options = ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument('--disable-application-cache')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("--disable-setuid-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--headless")

    def registrate(self) #-> а че возвращать то, надо подумать:
    try:

        pass

    def authorizate(self):
        pass
