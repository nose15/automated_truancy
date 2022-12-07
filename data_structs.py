from utils import Utils
import webbrowser


class DataTable:
    name = ""
    html_file_path = ""
    html = ""

    local_headers = []

    rows = []

    local_data = []

    def __init__(self, html, html_file_path, header_columns, header_rows):
        self.html = html
        self.html_file_path = html_file_path
        self.header_columns = header_columns
        self.header_rows = header_rows

        self.__save_html()
        rows = html.find_all("tr")

    def display(self):
        path = self.html_file_path.split('/')[-1]
        webbrowser.open_new_tab(path)

    def __save_html(self):
        with open(self.html_file_path, 'w') as file:
            file_html = str(self.html).replace("tbody", "table")
            file.write(str(file_html))

    def __get_html(self):
        with open(self.html_file_path) as file:
            html = file.read()
        return html

    def get_data_as_dict(self):
        data = {}

        table_headers = self.__extract_headers()
        table_row_data = self.__extract_data()

        for row in table_row_data:
            title = row[0]
            elements = row[1:]
            subject_data = {}

            for header in table_headers["term_headers"]:
                subject_data[header] = {}

            for idx, value in enumerate(elements):
                freq_header = table_headers["frequency_headers"][idx % len(table_headers["frequency_headers"])]
                term_header = table_headers["term_headers"][idx // len(table_headers["frequency_headers"])]

                subject_data[term_header][freq_header] = float(value)

            data[title] = subject_data

        return data

    def __extract_headers(self):
        headers = {"term_headers": [], "frequency_headers": []}
        keys = list(headers.keys())

        for tr_index, tr in enumerate(self.html.find_all("tr")):
            if tr.find("th"):
                tr_soup = Utils.soup_out_of_soup(tr)
                row_headers = Utils.cleared_elements_from_soup(tr_soup, "th")
                row_headers = Utils.clean_of_duplicates(row_headers)
                headers[keys[tr_index]] = row_headers

        return headers

    def __extract_data(self):
        row_data = []
        row_data_ = []
        for tr_index, tr in enumerate(self.html.find_all("tr")):
            tr_soup = Utils.soup_out_of_soup(tr)
            for td in tr_soup.find_all("td"):
                td_text = td.text

                if not td_text:
                    td_text = "0"
                row_data.append(td_text.strip())

        current_arr = []
        current_idx = 0
        for element in row_data[1:]:
            if current_idx > 21:
                current_idx = 0
                row_data_ .append(current_arr)
                current_arr = []

            current_arr.append(element)
            current_idx += 1

        return row_data_
