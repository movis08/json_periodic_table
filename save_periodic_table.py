import json
from pyquery import PyQuery as pq


def get_array_periodic_table():
    """
    Функция парсит сайт https://ru.wikipedia.org и собирает информацию об элементах
    переодической таблицы Менделеева

    :return: Массив
    """

    # Адрес сайта для склейки. Т.к. ссылки на сайте относительные
    base = 'https://ru.wikipedia.org'
    # Ссылка на первый элемент "Водород"
    url = 'https://ru.wikipedia.org/wiki/%D0%92%D0%BE%D0%B4%D0%BE%D1%80%D0%BE%D0%B4'

    next_arrow = '→'
    elements_list = []
    need_load_next_page = True
    while need_load_next_page:
        page = pq(url)
        # Блок в правой части страницы с подробной информацией об элементе
        inform_table_element = page(".mw-parser-output > table.infobox")
        # Ссылка на следующий и предыдущий элементы
        arrows_element = inform_table_element("tr:nth-child(2) td a")

        # Сбор данных о текущем элементе
        element_char = page(".mw-parser-output div:nth-child(1) div:nth-child(1) .mw-selflink")
        element_numb = page('.mw-parser-output div table[cellpadding="4"] tr:nth-child(1) td:nth-child(1)')
        element_name = page('.mw-parser-output div table[cellpadding="4"] tr:nth-child(1) td:nth-child(2)')

        # Преобразование данных корректным строкам
        element_char = pq(element_char[0]).text()
        element_numb = element_numb.text()
        element_name = element_name.text()

        elements_list.append({
            'elementChar': element_char,
            'elementNumb': element_numb,
            'elementName': element_name,
            'url': url
        })

        # Проверяем количество ссылок на другие элементы
        if len(arrows_element) == 1:
            first_arrow = arrows_element[0]
            if first_arrow.tail is not None:
                # Проверка что это не последний элемент
                if first_arrow.tail.find(next_arrow) != -1:
                    url = base + pq(first_arrow).attr('href')
                else:
                    need_load_next_page = False
            else:
                need_load_next_page = False
        elif len(arrows_element) == 2:
            second_arrow = arrows_element[1]
            url = base + pq(second_arrow).attr('href')
        else:
            # Ссылок нет. Закругляемся
            need_load_next_page = False

    return elements_list


if __name__ == '__main__':
    array_periodic_table = get_array_periodic_table()
    with open("periodic_table.json", "w") as json_file:
        json.dump(array_periodic_table, json_file)
