from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup

from scraping_tools import DataHarvester, AttendanceTableHarvester, TimetableHarvester
from data_structs import AttendanceDataTable, Timetable


def main():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    with open("credentials.txt") as credentials:
        lines = credentials.readlines()
        login = lines[0]
        password = lines[1]
        credentials.close()

    # data_collector = AttendanceTableHarvester(driver)
    # data_collector.set_page_url("https://lo12poznan.mobidziennik.pl/dziennik/statystykafrekwencji")
    # data_collector.set_login_and_password(True, login, password)
    # datatable_html = data_collector.harvest()
    #
    # soup = BeautifulSoup(datatable_html, "html.parser")
    #
    # data_table = AttendanceDataTable(soup, "data/frequency_data.html", "data/frequency_data.json")
    #
    # data_table.display()

    data_collector = TimetableHarvester(driver)
    data_collector.set_page_url("https://lo12poznan.mobidziennik.pl/dziennik/planlekcji?typ=podstawowy&tydzien=2023-01-09")
    data_collector.set_login_and_password(True, login, password)
    datatable_html = data_collector.harvest()

    soup = BeautifulSoup(datatable_html, "html.parser")

    timetable = Timetable(soup)


if __name__ == "__main__":
    main()
