from web import *
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

url_main_1 = 'https://clutch.co/uk/app-developers?page='
url_main_2 = '&related_services=&related_services=field_pp_sl_ecommerce'

columns = ['Company_names', 'Price']
apps_names_list_main = []
apps_price_list_main = []
apps_names_dict = dict()

for index in range(1, 10):
    code = requests.get(url_main_1 + str(index) + url_main_2)
    soup_code = bs(code.text, 'lxml')

    apps_names_list = soup_code.find_all('h3', {'class': 'company_info'})
    apps_price_list = soup_code.find_all('div', {'class': 'list-item block_tag custom_popover'})

    # apps_info_names = soup_code.find_all('div', {'class': 'h1'})
    # apps_info_languages = soup_code.find_all('ul', {'class': 'list-inline'})



    print(soup_code)

    for app_info in apps_names_list:
        apps_names_list_main.append(app_info.text.strip().replace('\n', ''))

    print(apps_price_list)

    apps_names_list_main.append(str(apps_price_list)[
                                str(apps_price_list).index('<span>$'):str(apps_price_list).index('</span>')])

    for index_1 in range(len(apps_names_list_main)):
        apps_names_dict[index_1] = dict()
        apps_names_dict[index_1]['Company_name'] = apps_names_list_main[index_1]
        apps_names_dict[index_1]['Price'] = apps_price_list_main[0]

    print(apps_names_dict)

    data_file = pd.DataFrame(data=apps_names_dict, index=columns).T
    data_file.to_csv('US_Companies_main.csv')

    print(f'Page {index} ready')

# data = pd.read_csv('UK_Companies.csv').T
# data_dict = data.to_dict()
#
# new_data = dict()
# for index in range(len(data_dict)):
#     new_data[index] = dict()
#     new_data[index] = data_dict[index]['Company_name']
#
# data_file = pd.DataFrame(data=new_data, index=['Company_name']).T
# data_file.to_csv('UK_Companies_1.csv')

# url_main_first = 'https://appropio.com/top-27-luchshih-sredstv-po-dlja-razrabotki-mobilnyh-prilozhenij/'
# url_main_second = 'https://www.softwareadvice.com/construction/best-apps-comparison/p/all/'
# url_main_third = 'https://wadline.com/mobile/gb?page='
#
# code = requests.get(url_main_third)
# soup_code = bs(code.text, 'lxml')
#
# all_results = []
# for index in range(1, 4):
#     print(index)

# apps_info = soup_code.find_all('div', {'class': 'full category'})
# print(len(apps_info))
#
# app_info = apps_info[0].find_all('div')
# print(len(app_info))
# for elem in app_info:
#     print(elem, end='\n\n')