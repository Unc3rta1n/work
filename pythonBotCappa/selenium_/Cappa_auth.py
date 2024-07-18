from selenium_.Cappa import *


class CappaAuth(Cappa):
    """Класс для авторизации пользователя на сайте cappa.csu.ru"""

    def __init__(self, username: str, password: str):
        super().__init__()
        self.username = username
        self.password = password

    def authorizate(self) -> str | None:  # сюда хочется какую то структуру, чтобы еще описание ошибки выводить
        try:
            with Edge(options=self.options) as driver:
                driver.get(self.url)
                time.sleep(2)

                cappa_button = driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[3]/div/a')
                cappa_button.click()
                time.sleep(2)
                # Перешли на  https://cappa.csu.ru/auth/signin/
                cappa_text_field = driver.find_element(By.XPATH, '//*[@id="id_login"]')
                cappa_text_field.click()
                cappa_text_field.send_keys(self.username)

                cappa_text_field = driver.find_element(By.XPATH, '//*[@id="id_password"]')
                cappa_text_field.click()
                cappa_text_field.send_keys(self.password)

                cappa_button = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/form/input[5]')
                cappa_button.click()

                time.sleep(2)

                if driver.current_url == 'https://cappa.csu.ru/':
                    print(f'Пользователь с логином {self.username} успешно авторизован')
                    return None
                else:
                    cappa_error = driver.find_element(By.XPATH,
                                                      '/html/body/div/main/div/div[2]/div/form/small')
                    print(cappa_error.text)
                    return cappa_error.text

        except Exception as e:
            print(f"Произошла какая то ошибка: {e}")
            return 'Неотловленная ошибка произошла'
