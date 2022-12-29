from utils import Utils
import webbrowser
import json
import os


class AttendanceDataTable:
    html_file_path = ""
    json_file_path = ""

    def __init__(self, html, html_file_path, json_file_path):
        self.html_file_path = html_file_path
        self.json_file_path = json_file_path

        self.__save_html(html)
        self.__save_json(html)

    def display(self):
        abs_cwd_path = os.getcwd().replace("/", "\\")
        local_html_path = "\\" + self.html_file_path.replace("/", "\\")
        path = abs_cwd_path + local_html_path
        webbrowser.open_new_tab(path)

    def __save_html(self, html):
        clean_html = str(html).replace("tbody", "table")
        with open(self.html_file_path, 'w') as file:
            file.write(str(clean_html))

    def __save_json(self, html):
        data_as_dict = self.__html_to_dict(html)
        data_json = json.dumps(data_as_dict)
        with open(self.json_file_path, 'w') as file:
            file.write(data_json)

    def __html_to_dict(self, html):
        data = {}

        table_headers = self.__extract_headers(html)
        table_row_data = self.__extract_data(html)

        for row in table_row_data:
            title = row[0]
            elements = row[1:]
            subject_data = {}

            for header in table_headers["term_headers"]:
                subject_data[header] = {}

            for idx, value in enumerate(elements):
                freq_header = table_headers["attendance_headers"][idx % len(table_headers["attendance_headers"])]
                term_header = table_headers["term_headers"][idx // len(table_headers["attendance_headers"])]

                subject_data[term_header][freq_header] = float(value)

            data[title] = subject_data

        return data

    def __get_html(self):
        with open(self.html_file_path) as file:
            html = file.read()
        return html

    def __extract_headers(self, html):
        headers = {"term_headers": [], "attendance_headers": []}
        keys = list(headers.keys())

        for tr_index, tr in enumerate(html.find_all("tr")):
            if tr.find("th"):
                tr_soup = Utils.soup_out_of_soup(tr)
                row_headers = Utils.cleared_elements_from_soup(tr_soup, "th")
                row_headers = Utils.clean_of_duplicates(row_headers)
                headers[keys[tr_index]] = row_headers

        return headers

    def __extract_data(self, html):
        row_data = []
        row_data_ = []
        for tr_index, tr in enumerate(html.find_all("tr")):
            tr_soup = Utils.soup_out_of_soup(tr)
            for td in tr_soup.find_all("td"):
                td_text = td.text

                if not td_text:
                    td_text = "0"
                row_data.append(td_text.strip())

        current_lst = []
        current_idx = 0
        for element in row_data[1:]:
            if current_idx > 21:
                current_idx = 0
                row_data_ .append(current_lst)
                current_lst = []

            current_lst.append(element)
            current_idx += 1

        return row_data_


class Timetable:
    def __init__(self, html):
        self.HTML = html

    def __extract_data(self):
        spans = self.HTML.find_all("span")[:-22]

        lessons = []
        for i in range(1, len(spans), 2):
            lessons.append(spans[i])

        clean_lessons = []
        for lesson in lessons:
            lesson_soup = Utils.soup_out_of_soup(lesson)
            clean_lessons.append(lesson_soup.get_text(" "))


class Subject:
    name: str
    teacher: str
    importance: float
    coolness: float

    def __init__(self, name, teacher, importance, coolness):
        self.name = name
        self.teacher = teacher
        self.importance = importance
        self.coolness = coolness


class Lesson:
    starting_time: str
    ending_time: str
    subject: Subject

    def __init__(self, name, teacher, importance, coolness):
        self.name = name
        self.teacher = teacher
        self.importance = importance
        self.coolness = coolness
