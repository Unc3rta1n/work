from selenium_.Cappa import *


class CappaReg(Cappa):
    """Класс для регистрации пользователя на сайте cappa.csu.ru"""

    def __init__(self, username: str, password: str, email: str, first_name: str, last_name: str):
        super().__init__()
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def registrate(self) -> str | None:
        try:
            with Edge(options=self.options) as driver:
                driver.get(self.url)
                time.sleep(2)

                cappa_button = driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[3]/div/a')
                cappa_button.click()
                time.sleep(2)
                # Перешли на  https://cappa.csu.ru/auth/signin/

                cappa_button = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/form/a')
                cappa_button.click()
                time.sleep(2)  # wait for the next page to load

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
                time.sleep(2)

                if driver.current_url == 'https://cappa.csu.ru/':
                    print(f'Пользователь с логином {self.username} успешно зарегистрирован')
                    return None
                else:
                    cappa_error = driver.find_element(By.XPATH,
                                                      '/html/body/div/main/div/div[2]/div/form/small/ul/li')
                    return cappa_error.text

        except Exception as e:
            print(f"Ошибка при регистрации: {e}")
            return 'Неотловленная ошибка произошла'
