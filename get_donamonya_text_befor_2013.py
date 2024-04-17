import requests
from bs4 import BeautifulSoup
import get_donamonya_text
import renamefilename_fullwidth_to_halfwidth
import os


def get_webpage_soup(webpage: str, encoding_way: str):
    response = requests.get(webpage)
    response.encoding = encoding_way
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_links_of_each_year(start_year=1999, end_year=2012):
    links = []
    for y in range(start_year, end_year + 1):
        if y < 2007:
            link_of_year = f'http://www.kinki-with-kids.com/razio-kids/razio-mokuzi{y % 100:02d}.htm'
        else:
            link_of_year = f'http://www.kinki-with-kids.com/razio-kids/razio-mokuzi{y % 100:02d}.html'
        links.append(link_of_year)
    return links


def get_text_content(tag):
    texts = []
    for child in tag.children:
        if isinstance(child, str):
            texts.append(child.strip())
        elif child.name == "br" or child.name == '\n':
            texts.append("\n")
        elif child.name == 'hr':
            texts.append("\n")
            texts.append("\n")
        elif child.name == "font" and child.get("size") == "-1":
            continue
        else:
            if child.name == 'p' or child.name == 'b':
                texts.append("\n")
            texts.extend(get_text_content(child))
    return texts


def modify_file_name(filename: str):
    temp = get_donamonya_text.sanitize_filename(filename)
    temp = renamefilename_fullwidth_to_halfwidth.fullwidth_to_halfwidth(temp)
    temp = temp.strip()
    modify_name = temp.replace('\n', '').replace('\\', '')
    return modify_name


def save_text_before_2013(start_year_int, end_year_int):
    doya_before_2013_path = 'doya_before_2013_download'
    if not os.path.exists(doya_before_2013_path):
        os.makedirs(doya_before_2013_path, exist_ok=True)

    # get the array of links of each year
    links_of_each_year = get_links_of_each_year(start_year_int, end_year_int)

    # get the dictionary of each year
    for link_of_each_year in links_of_each_year:
        each_year_soup = get_webpage_soup(link_of_each_year, 'UTF-8')
        links_in_each_year = dict()
        a_tags = each_year_soup.find_all(name='a')
        for a_tag in a_tags:
            link_of_month_short = str(a_tag.get('href'))
            link_of_month_long = f'http://www.kinki-with-kids.com/razio-kids/{link_of_month_short}'
            month_name_from_link = link_of_month_short.split('.')[0].split('-')

            if len(month_name_from_link) > 2:
                year_name = month_name_from_link[0].split('/')[1]
                month_name = month_name_from_link[1]
            else:
                year_name = month_name_from_link[0].split('/')[0]
                month_name = month_name_from_link[0].split('/')[1]
            year_name = modify_file_name(year_name)
            month_name = modify_file_name(month_name)

            day_name = a_tag.get_text().strip()
            day_name = modify_file_name(day_name)

            if day_name.endswith('月'):
                file_name = f'{year_name}年{month_name}月.txt'
            else:
                file_name = f'{year_name}年{month_name}月{day_name}.txt'

            links_in_each_year[file_name] = link_of_month_long
            print(f'file_name: {file_name}, link: {link_of_month_long}')

        # get the txt content of every webpage
        for file_name_of_txt_content, weblink_of_txt_content in links_in_each_year.items():
            text_content_soup = get_webpage_soup(weblink_of_txt_content, 'UTF-8')
            text_content_body = text_content_soup.find('body')
            text_content_list = get_text_content(text_content_body)

            file_path = os.path.join(doya_before_2013_path, file_name_of_txt_content)
            with open(file_path, 'w', encoding='utf-8') as file:
                for content in text_content_list:
                    file.write(str(content))
            print(f'save as {file_name_of_txt_content} in {file_path}')

if __name__ == '__main__':
    save_text_before_2013(1999, 2012)