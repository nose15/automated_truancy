from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup

from scraping_tools import DataHarvester
from data_structs import DataTable


def main():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    with open("credentials.txt") as credentials:
        lines = credentials.readlines()
        login = lines[0]
        password = lines[1]
        credentials.close()

    data_collector = DataHarvester(driver)
    data_collector.set_page_url("https://lo12poznan.mobidziennik.pl/dziennik/statystykafrekwencji")
    data_collector.set_login_and_password(True, login, password)
    datatable_html = data_collector.harvest()

    soup = BeautifulSoup(datatable_html, "html.parser")

    data_table = DataTable(soup, "data/frequency_data.html", "data/frequency_data.json")

    data_table.display()


if __name__ == "__main__":
    main()
