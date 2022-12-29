from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time


class DataHarvester:
    _website = ""

    _login_needed: bool
    _PAGE_URL: str
    _login: str
    _password: str

    def __init__(self, web_driver):
        self.web_driver = web_driver

    def set_page_url(self, page_url):
        self._PAGE_URL = page_url

    def set_login_and_password(self, login_needed: bool = True, login: str = "", password: str = ""):
        self._login_needed = login_needed
        self._login = login
        self._password = password

    def harvest(self) -> str:
        pass

    def _get_website(self):
        self.web_driver.get(self._PAGE_URL)
        time.sleep(0.5)
        self._log_in()
        time.sleep(1)
        self.web_driver.get(self._PAGE_URL)

    def _log_in(self):
        login_field = self.web_driver.find_element(by=By.ID, value="login")
        password_field = self.web_driver.find_element(by=By.ID, value="haslo")
        submit_button = self.web_driver.find_element(by=By.CLASS_NAME, value="zaloguj")

        time.sleep(0.1)
        login_field.send_keys(self._login)
        time.sleep(0.1)
        password_field.send_keys(self._password)
        time.sleep(0.1)
        submit_button.click()


class AttendanceTableHarvester(DataHarvester):
    def __init__(self, web_driver):
        super().__init__(web_driver)

    def harvest(self) -> str:
        access = False
        inner_html = None

        while access is False:
            try:
                table = self.web_driver.find_element(by=By.CLASS_NAME, value="spis")
                access = True
                inner_html = table.get_attribute('innerHTML')
            except NoSuchElementException:
                self._get_website()

        self.web_driver.close()

        return inner_html


class TimetableHarvester(DataHarvester):
    def __init__(self, web_driver):
        super().__init__(web_driver)

    def harvest(self) -> str:
        access = False
        inner_html = None

        while access is False:
            try:
                table = self.web_driver.find_element(by=By.CLASS_NAME, value="plansc_cnt")
                access = True
                inner_html = table.get_attribute('innerHTML')
            except NoSuchElementException:
                self._get_website()

        self.web_driver.close()

        return inner_html
