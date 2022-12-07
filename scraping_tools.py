from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import time




class DataHarvester:
    __website = ""

    __login_needed: bool
    __PAGE_URL: str
    __login: str
    __password: str

    def __init__(self, web_driver):
        self.web_driver = web_driver

    def set_page_url(self, page_url):
        self.__PAGE_URL = page_url

    def set_login_and_password(self, login_needed: bool = True, login: str = "", password: str = ""):
        self.__login_needed = login_needed
        self.__login = login
        self.__password = password

    def harvest(self) -> str:
        access = False
        inner_html = None

        while access is False:
            try:
                table = self.web_driver.find_element(by=By.CLASS_NAME, value="spis")
                access = True
                inner_html = table.get_attribute('innerHTML')
            except NoSuchElementException:
                self.__get_website()

        self.web_driver.close()

        return inner_html

    def __get_website(self):
        self.web_driver.get(self.__PAGE_URL)
        time.sleep(0.5)
        self.__log_in()
        time.sleep(1)
        self.web_driver.get(self.__PAGE_URL)

    def __log_in(self):
        login_field = self.web_driver.find_element(by=By.ID, value="login")
        password_field = self.web_driver.find_element(by=By.ID, value="haslo")
        submit_button = self.web_driver.find_element(by=By.CLASS_NAME, value="zaloguj")

        time.sleep(0.1)
        login_field.send_keys(self.__login)
        time.sleep(0.1)
        password_field.send_keys(self.__password)
        time.sleep(0.1)
        submit_button.click()


