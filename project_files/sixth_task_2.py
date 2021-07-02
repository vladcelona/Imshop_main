
from importing_modules import *


def download_file(url, verbose=False):
    # # local_filename = os.path.join('.', f"{url.split('/')[-1]}.xml")
    # if url.find(r'C:\Users\vladi') != -1:
    local_filename = os.path.join(f'{url.split("/")[-1]}.xml')
    # else:
    #     local_filename = os.path.join(rf"D:\{url.split('/')[-1]}.xml")

    # First version
    code = requests.get(url, stream=True)
    file_size = code.headers.get('content-length')

    chunk_size = 2 ** 14

    # Second version
    # user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    # headers = {'User-Agent': user_agent}
    # request = Request(url, headers=headers)
    # code = urlopen(request)
    # file_size = code.headers.get('content-length')
    # print(code.text)

    if file_size:
        file_size = int(file_size)
        num_bars = int(file_size / chunk_size)

        if verbose:
            print(f'File size: {file_size}')
            # print(dict(file_size=file_size))
            print(f'Number of bars: {num_bars}')
            # print(dict(num_bars=num_bars))

        with open(local_filename, 'wb') as open_file:
            for chunk in tqdm.tqdm(code.iter_content(chunk_size=chunk_size), total=num_bars, unit='MB',
                                   desc=local_filename, leave=True, ncols=100, ascii=True):
                open_file.write(chunk)

        return

    code_1 = requests.head(url, headers={'Accept-Encoding': None})
    file_size = code_1.headers.get('content-length')

    if file_size:
        file_size = int(file_size)
        num_bars = int(file_size / chunk_size)

        if verbose:
            print(f'File size: {file_size}')
            # print(dict(file_size=file_size))
            print(f'Number of bars: {num_bars}')
            # print(dict(num_bars=num_bars))

        with open(local_filename, 'wb') as open_file:
            for chunk in tqdm.tqdm(code.iter_content(chunk_size=chunk_size), total=num_bars, unit='MB',
                                   desc=local_filename, leave=True, ncols=100, ascii=True):
                open_file.write(chunk)

        return

    else:
        file_size = len(code_1.text.split('\n'))
        num_bars = int(file_size / 2 ** 14)
        with open(local_filename, 'wb') as open_file:
            for chunk in tqdm.tqdm(code.iter_content(chunk_size=8_192), desc=local_filename, total=num_bars,
                                   leave=True, ascii=True, ncols=100):
                open_file.write(chunk)

        return


def compile_task():
    url_main = sys.argv[1]
    # url_main = input('Input url of the page: ')
    download_file(url_main, verbose=True)
    # file_name = f'{url_main.split("/")[-1]}.xml'
    file_name = f'{url_main.split("/")[-1]}.xml'
    # file_size = os.stat(file_name).st_size

    tree = et.parse(file_name)
    root = tree.getroot()

    offers_errors = []  # 0
    pictures_errors = []  # 1
    prices_errors = []  # 2
    barcode_errors = []  # 3
    params_errors = []  # 4
    old_prices_errors = []  # 5
    retail_prices_errors = []  # 6
    description_errors = []  # 7
    rec_errors = []  # 8
    vat_errors = []  # 9
    badge_errors = []  # 10
    video_errors = []  # 11
    file_errors = []  # 12

    errors_list = []
    warnings_list = []
    infos_list = []

    errors_file_dir = 'feed_errors.txt'
    warnings_file_dir = 'feed_warnings.txt'
    infos_file_dir = 'feed_infos.txt'

    with open(file_name, 'r', encoding='utf-8') as open_file:
        code = open_file.readlines()

    def find_string(code, offer_id):
        for index in range(len(code)):
            if f'{offer_id}' in code[index] and '<offer' in code[index]:
                return index + 1

    def find_categories(category_id):
        nonlocal root, offers_found
        nonlocal errors_list, warnings_list, infos_list
        count = 0
        for categories in root[0].findall('categories'):
            for category in categories.findall('category'):
                if category.get('id') == category_id: count += 1
        if count == 0:
            errors_list.append(f"ID {offers_found[index_i].get('id')} (Строка "
                               f"{find_string(code, offers_found[index_i].get('id'))})"
                               f": Категория не представлена")

    def find_prices(price):
        if price is None:
            print("Error! No price found")

    # def write_info_file():
    #     nonlocal errors_file_dir, warnings_file_dir, infos_file_dir
    #     nonlocal errors_list, warnings_list, infos_list
    #     with open(errors_file_dir, 'a') as errors_file:
    #         errors_file.write('\n'.join(errors_list))
    #     with open(warnings_file_dir, 'a') as warnings_file:
    #         warnings_file.writelines('\n'.join(warnings_list))
    #     with open(infos_file_dir, 'a') as infos_file:
    #         infos_file.writelines('\n'.join(infos_list))

    # def find_prices(price):
    offers_found = root[0].findall('offers')[0]
    for index_i in tqdm.tqdm(range(len(offers_found.findall('offer'))), ncols=100, ascii=True, leave=True):
        find_categories(offers_found[index_i].find('categoryId').text)
        # print(offer.find('categoryId').text)
        offer_id = offers_found[index_i].get('id')
        if len(offers_found[index_i].findall('price')) < 1:
            errors_list.append(f"ID {offer_id} (Строка qqq666qqq): Цена")
        if len(offers_found[index_i].findall('picture')) < 1:
            errors_list.append(f"ID {offer_id} (Строка qqq666qqq): Картинки")
        if len(offers_found[index_i].findall('barcode')) < 1:
            warnings_list.append(f"ID {offer_id} (Строка qqq666qqq): Штрихкоды")
        if len(offers_found[index_i].findall('param')) < 1:
            warnings_list.append(f"ID {offer_id} (Строка qqq666qqq): Параметры")
        if len(offers_found[index_i].findall('oldPrice')) < 1:
            warnings_list.append(f"ID {offer_id} (Строка qqq666qqq): Старые цены")
        if len(offers_found[index_i].findall('retailPrice')) < 1:
            infos_list.append(f"ID {offer_id} (Строка qqq666qqq): РРЦ товара")
        if len(offers_found[index_i].findall('description')) < 1:
            warnings_list.append(f"ID {offer_id} (Строка qqq666qqq): Описание товара")
        if len(offers_found[index_i].findall('rec')) < 1:
            infos_list.append(f"ID {offer_id} (Строка qqq666qqq): Идентификаторы товаров")
        if len(offers_found[index_i].findall('vat')) < 1:
            warnings_list.append(f"ID {offer_id} (Строка qqq666qqq): Ставка НДС")
        if len(offers_found[index_i].findall('badge')) < 1:
            infos_list.append(f"ID {offer_id} (Строка qqq666qqq): Бейджик")
        if len(offers_found[index_i].findall('video')) < 1:
            infos_list.append(f"ID {offer_id} (Строка qqq666qqq): Видео")
        if len(offers_found[index_i].findall('file')) < 1:
            infos_list.append(f"ID {offer_id} (Строка qqq666qqq): Файл")
            # write_info_file()


    # for offer in offers_found.findall('offer'):
    #     print("OK", end=' ')

    print()

    # os.remove(errors_file_dir)
    # os.remove(warnings_file_dir)
    # os.remove(infos_file_dir)

    def replace_elements(info_list, info_type):
        description = ''
        if info_type == 'feed_errors.txt':
            description = 'Errors'
        elif info_type == 'feed_warnings.txt':
            description = 'Warnings'
        else:
            description = 'Info'
        for index in tqdm.tqdm(range(len(info_list)), ncols=100, ascii=True, leave=True, desc=description):
            # info_list[index] = info_list[index].replace('qqq666qqq',
            #                                             str(find_string(code, info_list[index].split()[1])))
            info_list[index] = re.sub('qqq666qqq',
                                      str(find_string(code, info_list[index].split()[1])), info_list[index])

        return info_list

    with open(errors_file_dir, 'w') as errors_file:
        errors_file.write('\n'.join(replace_elements(errors_list, errors_file_dir)))
    with open(warnings_file_dir, 'w') as warnings_file:
        warnings_file.writelines('\n'.join(replace_elements(warnings_list, warnings_file_dir)))
    with open(infos_file_dir, 'w') as infos_file:
        infos_file.writelines('\n'.join(replace_elements(infos_list, infos_file_dir)))

    # if len(errors_list) != 0:
    #     print("Errors: ")
    #     print(*errors_list, sep='\n')
    #     print()
    # if len(warnings_list) != 0:
    #     print("Warnings: ")
    #     print(*warnings_list, sep='\n')
    #     print()
    # if len(infos_list) != 0:
    #     print("Info: ")
    #     print(*infos_list, sep='\n')
    #     print()
    # if len(errors_list) == 0 and len(warnings_list) == 0 and len(infos_list) == 0:
    #     print("Ошибок не найдено")
    #     print()

    os.remove(file_name)
    os.startfile(errors_file_dir)
    os.startfile(warnings_file_dir)
    os.startfile(infos_file_dir)

    print("Конец обоработки файла")


def division_info_categories():
    error_string = []
    warning_string = []
    info_string = []


# def xml_feeds_1():
#     files_list = ['yandex_utm', 'mobileapp']
#
#     for file in files_list:
#         new_warnings_filename = 'Yandex%20Kiehls' + '_we1'
#         warnings_list = []
#         try:
#             with open('Yandex%20Kiehls.xml.xml', 'r', encoding='utf-8') as open_file:
#                 code = ''.join(open_file.readlines())
#         except Exception:
#             with open('Yandex%20Kiehls.xml.xml', 'r') as open_file:
#                 code = ''.join(open_file.readlines())
#
#         soup_code = bs(code, 'lxml')
#         offers_found = soup_code.find_all('offer')
#         print(len(offers_found))
#
#         for index in range(len(offers_found)):
#             print(index, end=' ')
#             found = offers_found[index].find_all('categoryid')
#             if len(soup_code.find_all('category', {'id': found[0].text})) == 0:
#                 warnings_list.append(f'No category found [{offers_found[index]["id"]}: {found[0].text}]\n')
#             if len(found) > 1:
#                 if len(soup_code.find_all('category', {'id': found[1].text})) == 0:
#                     warnings_list.append(f'No category found [{offers_found[index]["id"]}: {found[1].text}]\n')
#
#             with open(rf'C:\Users\Vlad04\Downloads\{new_warnings_filename}.txt',
#                           'w', encoding='utf-8') as open_file_1:
#                 open_file_1.writelines(warnings_list)
#
#         print()
#         print('Tags are done!')
#
#         c = 0
#         for index in range(len(offers_found)):
#             if len(offers_found[index].find_all('picture')) < 1:  # Чтобы найти price, просто меняешь picture :D
#                 # print(offers_found[index].find('categoryid').text)
#                 # print('Error', index)
#                 # print(offers_found[index])
#                 warnings_list.append(f'No image found in offer id: {offers_found[index]["id"]}\n')
#                 with open(f'{new_warnings_filename}.txt', 'w',
#                           encoding='utf-8') as open_file_1:
#                     open_file_1.writelines(warnings_list)
#
#         for index in range(len(offers_found)):
#             if len(offers_found[index].find_all('price')) < 1:  # Чтобы найти price, просто меняешь picture :D
#                 # print(offers_found[index].find('categoryid').text)
#                 # print('Error', index)
#                 # print(offers_found[index])
#                 warnings_list.append(f'No price found in offer id: {offers_found[index]["id"]}\n')
#                 with open(f'{new_warnings_filename}.txt', 'w',
#                           encoding='utf-8') as open_file_1:
#                     open_file_1.writelines(warnings_list)
#
#         # with open(rf'C:\Users\Vlad04\Downloads\{new_warnings_filename}.txt', 'w', encoding='utf-8') as open_file_1:
#         #     open_file_1.writelines(warnings_list)
#         os.startfile(f'{new_warnings_filename}.txt')


# if __name__ == '__main__':
# download_file('https://kiehls.ru/media/feed/Yandex%20Kiehls.xml', verbose=True)
# xml_feeds()
# xml_feeds_1()
# <warning>No pictures found</warning>
# 4945
# python main.py https://www.forward-sport.ru/bitrix/catalog_export/forward_stocks_250650.php


# def compile_task():
#     url_main = 'https://xn--80ae2aeeogi5fxc.xn--p1ai/feed/yml/imshop_catalog'
#     warnings_list = []
#
#     # code = requests.get(url_main)
#     with open(r'C:\Users\vladi\Downloads\imshop_catalog.xml', 'r', encoding='utf-8') as open_file:
#         code = ''.join(open_file.readlines())
#     print('Downloaded')
#     soup_code = bs(code, 'lxml')
#     print('Parsed')
#
#     offers_found = soup_code.find_all('offer')
#
#     # count_0 = 0
#     # count_1 = 0
#     # for index in range(len(offers_found)):
#     #     if offers_found[index]['available'] == 'true':
#     #         count_0 += 1
#     #     if int(offers_found[index].find('quantity').text) > 0:
#     #         count_1 += 1
#     #
#     # print(count_0)
#     # print(count_1)
#
#     for index in range(len(offers_found)):
#         print(index, end=' ')
#         found = offers_found[index].find_all('categoryid')
#         if len(soup_code.find_all('category', {'id': found[0].text})) == 0:
#             warnings_list.append(f'No category found [{offers_found[index]["id"]}: {found[0].text}]\n')
#         if len(found) > 1:
#             if len(soup_code.find_all('category', {'id': found[1].text})) == 0:
#                 warnings_list.append(f'No category found [{offers_found[index]["id"]}: {found[1].text}]\n')
#         with open(f'forward_errors_1.txt', 'w', encoding='utf-8') as open_file_1:
#             open_file_1.writelines(warnings_list)
#
#     print()
#     print('Tags are done!')
#
#     for index in range(len(offers_found)):
#         if len(offers_found[index].find_all('picture')) < 1:  # Чтобы найти price, просто меняешь picture :D
#             # print(offers_found[index].find('categoryid').text)
#             # print('Error', index)
#             # print(offers_found[index])
#             warnings_list.append(f'No image found in offer id: {offers_found[index]["id"]}\n')
#             with open(f'forward_errors_1.txt', 'w',
#                       encoding='utf-8') as open_file_1:
#                 open_file_1.writelines(warnings_list)
#
#     for index in range(len(offers_found)):
#         if len(offers_found[index].find_all('price')) < 1:  # Чтобы найти price, просто меняешь picture :D
#             # print(offers_found[index].find('categoryid').text)
#             # print('Error', index)
#             # print(offers_found[index])
#             warnings_list.append(f'No price found in offer id: {offers_found[index]["id"]}\n')
#             with open(f'forward_errors_1.txt', 'w',
#                       encoding='utf-8') as open_file_1:
#                 open_file_1.writelines(warnings_list)
#
#     os.startfile('forward_errors_1.txt')


if __name__ == '__main__':
    compile_task()
    print('First task completed!', end='\n')
    print('-=' * 20, end='\n')