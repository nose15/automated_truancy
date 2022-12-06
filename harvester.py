from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import webbrowser

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)


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


dataCollector = DataHarvester(driver)
dataCollector.set_page_url("https://lo12poznan.mobidziennik.pl/dziennik/statystykafrekwencji")
dataCollector.set_login_and_password(True, "ljanczak", "exCJWnJx")
datatable_html = dataCollector.harvest()

soup = BeautifulSoup(datatable_html, "html.parser")

records = soup.find_all("tr")[2:]

data = {}

term_headers = ["I okres", "II okres", "Caly Rok"]
headers = ["obecnosci", "spoznienia", "zwolnienia", "usprawiedliwione", "nieusprawiedliwione", "ogolnie", "FREKWENCJA"]

for record in records:
    record_str = str(record)
    record_soup = BeautifulSoup(record_str, "html.parser")
    table_data = record_soup.find_all("td")
    title = table_data[0].text
    subject_data = {"I okres": {}, "II okres": {}, "Caly Rok": {}}

    for idx, podata in enumerate(table_data[1:]):
        header = headers[idx % len(headers)]
        term_header = term_headers[idx // len(headers)]
        podata_text = podata.text
        if podata_text == "":
            podata_text = "0"

        subject_data[term_header][header] = float(podata_text)

    data[title] = subject_data


print(data)


class DataTable:
    name = ""
    html_file_path = ""
    html = ""
    rows = []

    def __init__(self, html, html_file_path, header_columns, header_rows):
        self.html = html
        self.html_file_path = html_file_path
        self.header_columns = header_columns
        self.header_rows = header_rows

        self.__save_html()
        rows = html.find_all("tr")
        print(rows)
        pass

    def display(self):
        path = self.html_file_path.split('/')[-1]
        webbrowser.open_new_tab(path)
        pass

    def __save_html(self):
        with open(self.html_file_path, 'w') as file:
            self.html = str(self.html).replace("tbody", "table")
            file.write(str(self.html))

    def __get_html(self):
        with open(self.html_file_path) as file:
            html = file.read()
        return html

    def get_data(self):
        pass


data_table = DataTable(soup, "./dupa.html")
data_table.display()








# get the website
# access the account
# gather data
# process data
# give output
