
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


class CappaReg(Cappa):
    """Класс для регистрации пользователя на сайте cappa.csu.ru"""

    def __init__(self, username: str, password: str, email: str, first_name: str, last_name: str):
        super().__init__()  # Вызовите __init__ базового класса
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def registrate(self):
        try:
            with Edge(options=self.options) as driver:
                driver.get(self.url)
                time.sleep(2)  # wait for page to load
                driver.save_screenshot('step1_initial_load.png')

                cappa_button = driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[3]/div/a')
                cappa_button.click()
                time.sleep(2)  # wait for the next page to load
                driver.save_screenshot('step2_after_first_click.png')
                # Перешли на  https://cappa.csu.ru/auth/signin/
                cappa_button = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/form/a')
                cappa_button.click()
                time.sleep(2)  # wait for the next page to load
                driver.save_screenshot('step3_after_second_click.png')
                # Перешли на https://cappa.csu.ru/auth/signup/

                fields = {
                    '//*[@id="id_username"]': self.username,
                    '//*[@id="id_email"]': self.email,
                    '//*[@id="id_first_name"]': self.first_name,
                    '//*[@id="id_last_name"]': self.last_name,
                    '//*[@id="id_password1"]': self.password,
                    '//*[@id="id_password2"]': self.password,
                }

                for xpath, value in fields.items():
                    cappa_text_field = driver.find_element(By.XPATH, xpath)
                    cappa_text_field.click()
                    cappa_text_field.send_keys(value)

                # клик на кнопку регистрации
                cappa_button = driver.find_element(By.XPATH,
                                                   '/html/body/div/main/div/div[2]/div/form/input[3]')
                cappa_button.click()
                time.sleep(2)  # wait for the next page to load
                driver.save_screenshot('step10_after_registration_click.png')
                if driver.current_url == 'https://cappa.csu.ru/':
                    print(f'Пользователь с логином {self.username} успешно зарегистрирован')
                else:
                    print(f'Произошла какая-то ошибка')
                    cappa_error = driver.find_element(By.XPATH,
                                                      '/html/body/div/main/div/div[2]/div/form/small/ul/li')
                    print(cappa_error.text)

        except Exception as e:
            print(f"Ошибка при регистрации: {e}")

    def authorizate(self):
        try:
            with Edge(options=self.options) as driver:
                driver.get(self.url)

        except Exception as e:
            print(f"Ошибка при авторизации: {e}")


Cappa = CappaReg('sakldadkl123akdlsajkldasjkldasd', '123', 'dsaddsa11dsa@ya.ru', 'sdadsadsa', 'daadsdasadsdas')
Cappa.registrate()
