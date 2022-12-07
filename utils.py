from bs4 import BeautifulSoup


class Utils:
    @staticmethod
    def clean_of_duplicates(item_list):
        clear_list = []
        for item_index, list_item in enumerate(item_list):
            if list_item not in clear_list:
                clear_list.append(list_item)

        return clear_list

    @staticmethod
    def cleared_elements_from_soup(soup_arg, element_tag):
        elements = []

        for element in soup_arg.find_all(element_tag):
            element_text = element.text.strip()
            if element_text:
                elements.append(element_text)

        return elements

    @staticmethod
    def soup_out_of_soup(soup_arg):
        soup_str = str(soup_arg)
        new_soup = BeautifulSoup(soup_str, "html.parser")

        return new_soup
