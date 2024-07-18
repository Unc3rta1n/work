from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
import time


class Cappa:
    def __init__(self):
        self.url = "https://cappa.csu.ru/"
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
