import time
import random
from bs4 import BeautifulSoup
import requests
import datetime
import os

# Fetch the webpage, and pass it to BeautifulSoup.
def get_webpage_soup(weblink):
    # send a GET request to fetch the webpage of list
    response = requests.get(weblink)
    
    # add headers to the request to let the server know that i am using a mobile browser
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"}

    response = requests.get(weblink, headers = headers)

    # parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# the type of start_month and dend_month is datetime
def get_links_dict(start_month, end_month):
    index_link = 'http://radioxxxkids.blog.fc2.com/?mp=223413'

    index_link_soup = get_webpage_soup(index_link)

    # Find the <ul class="plugin_list"> element.
    list_element = index_link_soup.find("ul", {"class": "plugin_list"})

    # Initialize the result dictionary.
    links_dict = {}

    for child in list_element.descendants:
        if child.name == "a" and child.has_attr("href"):
            # Get the string representation of the href attribute, which is the URL for each month.
            month_href_str = str(child["href"])

            month_str = month_href_str.split("=")[-1]
            month_str_datetime = datetime.datetime.strptime(month_str, "%Y%m")
            
            # Filter out the URLs of the text content for dates
            # date between start_moth and end_month
            if (month_str_datetime.year > start_month.year or (month_str_datetime.year == start_month.year and month_str_datetime.month >= start_month.month)) and \
                (month_str_datetime.year < end_month.year or (month_str_datetime.year == end_month.year and month_str_datetime.month <= end_month.month)):

                # Store the href string as the value, with the key as the key-value pair, in the dictionary
                links_dict[month_str] = month_href_str

    return links_dict

def get_inner_text(entry_tag):
    if isinstance(entry_tag, str):
        return [entry_tag]
    if entry_tag.name == 'br':
        return ['\n']
    if 'class' in entry_tag.attrs and 'fc2_footer' in entry_tag.attrs['class']:
        return None
    if 'class' in entry_tag.attrs and 'entry_info' in entry_tag.attrs['class']:
        return None
    if entry_tag.name in {'span', 'strong', 'div', 'section','img','font'}:
        text_res = []
        for child in entry_tag.children:
            doya_text = get_inner_text(child)
            if doya_text is None or len(doya_text) == 0:
                continue
            else:
                if text_res and doya_text[0] != '\n':
                    text_res[-1] += doya_text[0]
                else:
                    text_res.append(doya_text[0])
                text_res.extend(doya_text[1:])
        
        return text_res

def get_entry_text(doya_soup, attr_entry: str):
    text_contents = []
    entry_tag = doya_soup.find('section', class_=attr_entry)
    if entry_tag is not None:
        text_contents = get_inner_text(entry_tag)
    return text_contents

def sanitize_filename(filename):
    illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

    for char in illegal_chars:
        filename = filename.replace(char, '_')

    return filename

# def save_text(start_date):
def save_text(start_date, end_date, path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    links_dict = get_links_dict(start_date, end_date)

    for value in links_dict.values():
        # Generate a random interval between 3 and 6 seconds
        interval = random.uniform(1, 4)
        # Wait for the random interval
        time.sleep(interval)

        one_month_soup = get_webpage_soup(value)

        # Create a dictionary to store all articles that need to be stored for the current month.
        doya_pages = {}
  
        def get_page_inner_link(soup):
            # Find all elements `<ul>` with the class `entry_list`.
            ul_entries = one_month_soup.find_all('ul', class_='entry_list')

            for ul_entry in ul_entries:
                a_tags = ul_entry.find_all('a')
                # Iterate through all <a> tags, which are links to each article.
                for a_tag in a_tags:
                    link = a_tag['href']
                    key = a_tag.find('strong').text.strip()
                    # Store the links in a dictionary, with the date as the key-value pair's key and the link as the value.
                    doya_pages[key] = link
            return doya_pages

        # Store the links of each page that needs to be traversed.
        pager_div = one_month_soup.find('div', class_='pager')
        
        if pager_div is not None:
            one_month_pages_links = []
            pages_a_tags = pager_div.find_all('a')
            for pages_a_tag in pages_a_tags:
                page_link = pages_a_tag['href']
                one_month_pages_links.append(page_link)
            for one_month_pages_link in one_month_pages_links:
                one_month_pages_soup = get_webpage_soup(one_month_pages_link)
                doya_pages_temp = get_page_inner_link(one_month_pages_soup)
                doya_pages.update(doya_pages_temp)
        else:
            doya_pages = get_page_inner_link(one_month_soup)

        for file_name, page_link in doya_pages.items():
            doya_day_page_soup = get_webpage_soup(page_link)
            print(page_link)
            doya_text = get_entry_text(doya_day_page_soup, 'entry')
            
            # If the folder does not exist, create it
            if not os.path.exists(path):
                os.makedirs(path)
            
            file_name = sanitize_filename(file_name)
            # Concatenate the complete path of the file
            file_path = os.path.join(path, f'{file_name}.txt')

            with open(file_path, 'w', encoding='utf-8') as file:
                start_to_write = False
                for i, content in enumerate(doya_text):
                    if doya_text[i] != '\n':
                        start_to_write = True
                    if start_to_write:
                        file.write(content)
            print(f'save as {file_name}.txt in {file_path}')

if __name__ == '__main__':
    start_date = datetime.datetime.strptime('19950301', "%Y%m%d")
    end_date = datetime.datetime.strptime('20071001', "%Y%m%d")
    save_text(start_date, end_date, 'doya_text_download')