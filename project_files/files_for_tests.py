from urllib.request import urlopen
from urllib.request import Request
import requests
import urllib3


def open_file():
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}

    code_1 = requests.head('https://kiehls.ru/media/feed/Yandex%20Kiehls.xml', headers={'Accept-Encoding': None})
    print(code_1.headers.get('content-length'))
    # code = urlopen('http://8203d5fd-6010-420e-8616-d478fb6422cc.selcdn.net/clients/respect/catalog.xml').info()
    request = Request('https://kiehls.ru/media/feed/Yandex%20Kiehls.xml', headers=headers)
    code = urlopen(request)
    # print(code.read().decode('utf-8'))
    # print(code.info())


if __name__ == '__main__':
    open_file()