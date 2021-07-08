
from importing_modules import *


def download_file(url, verbose=False):
    # # local_filename = os.path.join('.', f"{url.split('/')[-1]}.xml")
    # if url.find(r'C:\Users\vladi') != -1:
    local_filename = os.path.join(f'{url.split("/")[-1]}.xml')
    if local_filename.count('?') > 0 or local_filename.count('=') > 0:
        local_filename = 'file_name_for_parsing.xml'
    # else:
    #     local_filename = os.path.join(rf"D:\{url.split('/')[-1]}.xml")

    # First version
    code = requests.get(url, stream=True)
    file_size = code.headers.get('content-length')

    chunk_size = 2 ** 16

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
    file_name = f'{url_main.split("/")[-1]}.xml'
    # file_name = os.path.join(f'{url_main.split("/")[-1]}.xml')
    # file_name = 'catalog.xml.xml'
    if file_name.count('?') > 0 or file_name.count('=') > 0:
        file_name = 'file_name_for_parsing.xml'
    # file_size = os.stat(file_name).st_size

    default_line = -1

    # file_name = r'C:\Users\Vlad04\Downloads\Telegram Desktop\mobileapp.xml'

    errors_file_dir = 'feed_errors_3.txt'
    warnings_file_dir = 'feed_warnings_3.txt'
    infos_file_dir = 'feed_infos_3.txt'

    try:
        os.remove(errors_file_dir)
        os.remove(warnings_file_dir)
        os.remove(infos_file_dir)
    except FileNotFoundError:
        pass

    def replace_elements(info_list, info_type):
        description = ''
        if info_type == 'feed_errors.txt':
            description = 'Errors'
        elif info_type == 'feed_warnings.txt':
            description = 'Warnings'
        else:
            description = 'Info'

        # for index in tqdm.tqdm(range(len(info_list)), ncols=100, ascii=True, leave=True, desc=description):
        #     # info_list[index] = info_list[index].replace('{offer_line}',
        #     #                                             str(find_string(code, info_list[index].split()[1])))
        #     info_list[index] = re.sub('{offer_line}',
        #                               str(find_string(code, info_list[index].split()[1])), info_list[index])

        return info_list

    errors_list = []
    warnings_list = []
    infos_list = []

    errors_append = errors_list.append
    warnings_append = warnings_list.append
    infos_append = infos_list.append

    ids_dict = {elem.split()[0]: elem.split()[2] for elem in open("lines_found.txt").readlines()}

    try:
        errors_file = open(errors_file_dir, 'a', encoding='utf-8')
        errors_write = errors_file.write

        ids_list = []
        root = ' '
        tree = et.iterparse(file_name, events=('start', 'end'))
        for index, (event, elem) in tqdm.tqdm(enumerate(tree), ncols=100, leave=True):
            if index == 0:
                root = elem
            if event == 'end' and elem.tag == 'category':
                ids_list.append(elem.get('id'))
            if event == 'end' and elem.tag == 'offer':
                try:
                    default_string = f"ID {elem.get('id')} (Строка {ids_dict[elem.get('id')]}): ["
                except KeyError:
                    default_string = f"ID {elem.get('id')}: ["
                if elem.find('categoryId').text not in ids_list:
                    default_string += "Категория, "
                if not len(elem.findall('price')):
                    default_string += "Цена, "
                if not len(elem.findall('picture')):
                    default_string += "Картинки\n"
                default_string += ']\n'
                if '[]' in default_string:
                    default_string = f"ID {elem.get('id')}: Ошибок не найдено"
                else:
                    errors_write(default_string)
            root.clear()
            # if len(errors_list) != 0:
            #     with open(errors_file_dir, 'a') as errors_file:
            #         errors_file.write(''.join(replace_elements(errors_list, errors_file_dir)))
            #     errors_list = []
            # if len(warnings_list) != 0:
            #     with open(warnings_file_dir, 'a') as warnings_file:
            #         warnings_file.writelines(''.join(replace_elements(warnings_list, warnings_file_dir)))
            #     warnings_list = []
            # if len(infos_list) != 0:
            #     with open(infos_file_dir, 'a') as infos_file:
            #         infos_file.writelines(''.join(replace_elements(infos_list, infos_file_dir)))
            #     infos_list = []

        # print(len(ids_list))

        errors_file.close()

        time.sleep(5)

        warnings_file = open(warnings_file_dir, 'a', encoding='utf-8')
        warnings_write = warnings_file.write

        ids_list = []
        root = ' '
        tree = et.iterparse(file_name, events=('start', 'end'))
        for index, (event, elem) in tqdm.tqdm(enumerate(tree), ncols=100, leave=True):
            if index == 0:
                root = elem
            if event == 'end' and elem.tag == 'category':
                ids_list.append(elem.get('id'))
            if event == 'end' and elem.tag == 'offer':
                try:
                    default_string = f"ID {elem.get('id')} (Строка {ids_dict[elem.get('id')]}): ["
                except KeyError:
                    default_string = f"ID {elem.get('id')}: ["
                if not len(elem.findall('barcode')):
                    default_string += "Штрихкоды, "
                if not len(elem.findall('param')):
                    default_string += "Параметры, "
                if not len(elem.findall('oldPrice')) and not len(elem.findall('oldprice')):
                    default_string += "Старые цены, "
                if not len(elem.findall('description')):
                    default_string += "Описание товара, "
                if not len(elem.findall('vat')):
                    default_string += "Ставка НДС, "
                if not len(elem.findall('quantity')):
                    default_string += "Количество, "
                default_string += ']\n'
                if '[]' in default_string:
                    default_string = f"ID {elem.get('id')}: Предупреждений не найдено"
                else:
                    warnings_write(default_string)
            root.clear()

        warnings_file.close()

        time.sleep(5)

        infos_file = open(infos_file_dir, 'a', encoding='utf-8')
        infos_write = infos_file.write

        ids_list = []
        root = ' '
        tree = et.iterparse(file_name, events=('start', 'end'))
        for index, (event, elem) in tqdm.tqdm(enumerate(tree), ncols=100, leave=True):
            if index == 0:
                root = elem
            if event == 'end' and elem.tag == 'category':
                ids_list.append(elem.get('id'))
            if event == 'end' and elem.tag == 'offer':
                try:
                    default_string = f"ID {elem.get('id')} (Строка {ids_dict[elem.get('id')]}): ["
                except KeyError:
                    default_string = f"ID {elem.get('id')}: ["
                if not len(elem.findall('retailPrice')):
                    default_string += "РРЦ товара, "
                if not len(elem.findall('rec')):
                    default_string += "Идентификаторы товаров, "
                if not len(elem.findall('badge')):
                    default_string += "Бейджик, "
                if not len(elem.findall('video')):
                    default_string += "Видео, "
                if not len(elem.findall('file')):
                    default_string += "Файл, "
                default_string += ']\n'
                if '[]' in default_string:
                    default_string = f"ID {elem.get('id')}: Ошибок не найдено"
                else:
                    infos_write(default_string)
            root.clear()

        infos_file.close()
    except parse_error:
        os.remove(file_name)
        print()
        print("Error! This file does not have at least one closing element!")
        print("Soon there will be self-closing elements programme")
        return

    # with open(file_name, 'r', encoding='utf-8') as open_file:
    #     index_line = 1
    #     for line in open_file:
    #         if '<offer' in line:
    #             for index in range(len(errors_list)):
    #                 if (errors_list[index].split()[1]) in line:
    #                     errors_list[index] = errors_list[index]
    #             for index in range(len(warnings_list)):
    #                 if warnings_list[index].split()[1] in line:
    #                     warnings_list[index] = warnings_list[index]
    #             for index in range(len(infos_list)):
    #                 if infos_list[index].split()[1] in line:
    #                     infos_list[index] = infos_list[index]
    #         index_line += 1

    # with open(errors_file_dir, 'w') as errors_file:
    #     errors_file.write(''.join(replace_elements(errors_list, errors_file_dir)))
    # with open(warnings_file_dir, 'w') as warnings_file:
    #     warnings_file.writelines(''.join(replace_elements(warnings_list, warnings_file_dir)))
    # with open(infos_file_dir, 'w') as infos_file:
    #     infos_file.writelines(''.join(replace_elements(infos_list, infos_file_dir)))

    # os.remove(file_name)

    os.startfile(errors_file_dir)
    os.startfile(warnings_file_dir)
    os.startfile(infos_file_dir)


if __name__ == '__main__':
    compile_task()