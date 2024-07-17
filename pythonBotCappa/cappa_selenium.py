import selenium
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CappaRegAuth:
    """Класс для регистрации\\авторизации пользователя на сайте cappa.csu.ru"""

    def __init__(self, username: str, password: str, email: str, first_name: str, last_name: str):
        self.url = "https://cappa.csu.ru/"
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

        self.options = EdgeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        #self.options.add_argument("--no-sandbox")
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

                # Теперь заполняем 6 полей на сайте полями из класса
                cappa_text_field = driver.find_element(By.XPATH, '//*[@id="id_username"]')
                cappa_text_field.click()
                cappa_text_field.send_keys(self.username)
                driver.save_screenshot('step4_after_username.png')

                cappa_text_field = driver.find_element(By.XPATH, '//*[@id="id_email"]')
                cappa_text_field.click()
                cappa_text_field.send_keys(self.email)
                driver.save_screenshot('step5_after_email.png')

                cappa_text_field = driver.find_element(By.XPATH, '//*[@id="id_first_name"]')
                cappa_text_field.click()
                cappa_text_field.send_keys(self.first_name)
                driver.save_screenshot('step6_after_first_name.png')

                cappa_text_field = driver.find_element(By.XPATH, '//*[@id="id_last_name"]')
                cappa_text_field.click()
                cappa_text_field.send_keys(self.last_name)
                driver.save_screenshot('step7_after_last_name.png')

                cappa_text_field = driver.find_element(By.XPATH, '//*[@id="id_password1"]')
                cappa_text_field.click()
                cappa_text_field.send_keys(self.password)
                driver.save_screenshot('step8_after_password1.png')

                cappa_text_field = driver.find_element(By.XPATH, '//*[@id="id_password2"]')
                cappa_text_field.click()
                cappa_text_field.send_keys(self.password)
                driver.save_screenshot('step9_after_password2.png')
                # клик на кнопку регистрации
                cappa_button = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/form/input[3]')
                cappa_button.click()
                time.sleep(2)  # wait for the next page to load
                driver.save_screenshot('step10_after_registration_click.png')
                # ну и как бы вроде как зарегались но не понятно

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


Cappa = CappaRegAuth('sakldadklakdlsajkldasjkldasd', '12345', 'dsaddsadsa@ya.ru', 'sdadsadsa', 'daadsdasadsdas')
Cappa.registrate()
