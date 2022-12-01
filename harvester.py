from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

import time
from selenium import webdriver
driver = webdriver.Firefox()


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
        self.__get_website()

        table = self.web_driver.find_element(by=By.CLASS_NAME, value="spis")
        inner_html = table.get_attribute('innerHTML')
        self.web_driver.close()

        return inner_html

    def __get_website(self):
        self.web_driver.get(self.__PAGE_URL)
        time.sleep(0.1)
        self.__log_in()
        time.sleep(0.1)
        self.web_driver.get(self.__PAGE_URL)
        time.sleep(0.1)

    def __log_in(self):
        login_field = self.web_driver.find_element(by=By.ID, value="login")
        password_field = self.web_driver.find_element(by=By.ID, value="haslo")
        submit_button = self.web_driver.find_element(by=By.CLASS_NAME, value="zaloguj")

        login_field.send_keys(self.__login)
        password_field.send_keys(self.__password)
        submit_button.click()


dataCollector = DataHarvester(driver)
dataCollector.set_page_url("https://lo12poznan.mobidziennik.pl/dziennik/statystykafrekwencji")
dataCollector.set_login_and_password(True, "ljanczak", "exCJWnJx")
datatable_html = dataCollector.harvest()
print(BeautifulSoup(datatable_html, "html.parser").current_data)



# get the website
# access the account
# gather data
# process data
# give output
