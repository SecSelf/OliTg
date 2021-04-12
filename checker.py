from bs4 import BeautifulSoup
import requests
from db import get_app_link, change_flag


def parse_2(url: str):
    url_error = 'URL is not correct'
    name_error = 'Невозможно получить имя приложения, попробуйте другую ссылку.'
    try:
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.169 Safari/537.36'
        }
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        app_name = soup.find('h1', class_='AHFaub').text
       #app_rate = soup.find('div', class_='pf5lIe').find('div', role='img')
        article_title = soup.find('div', class_='uaxL4e')
        if article_title is None:
            return app_name
        else:
            return app_name
    except requests.exceptions.MissingSchema:
        return url_error
    except AttributeError:
        return name_error


async def parse_test():
        get_link = get_app_link()
        ax = len(get_link)
        m = 0
        for i in range(ax):
            for a in get_link[m]:
                URL = a
                HEADERS = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                          'Chrome/74.0.3729.169 Safari/537.36'
                        }
                response = requests.get(URL, headers=HEADERS)
                soup = BeautifulSoup(response.content, 'html.parser')
                article_title = soup.find('div', class_='uaxL4e')
                m += 1
                if article_title is None:
                    print('App ' + URL + ' is working')
                else:
                    change_flag(url= URL)
                    print('App ' + URL + ' is not available')


