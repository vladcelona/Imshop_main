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
    # file_name = f'{url_main.split("/")[-1]}.xml'
    file_name = os.path.join(f'{url_main.split("/")[-1]}.xml')
    if file_name.count('?') > 0 or file_name.count('=') > 0:
        file_name = 'file_name_for_parsing.xml'
    # file_size = os.stat(file_name).st_size

    default_line = -1

    # file_name = r'C:\Users\Vlad04\Downloads\Telegram Desktop\mobileapp.xml'

    try:
        tree = et.parse(file_name)
        root = tree.getroot()
    except parse_error:
        os.remove(file_name)
        print()
        print("Error! This file does not have at least one closing element!")
        print("Soon there will be self-closing elements programme")
        return

    errors_list = []
    warnings_list = []
    infos_list = []

    errors_file_dir = 'feed_errors_1.txt'
    warnings_file_dir = 'feed_warnings_1.txt'
    infos_file_dir = 'feed_infos_1.txt'

    all_categories_found = root[0].findall('categories')[0].findall('category')
    # all_ids_found = root[0].findall('availability')[0].findall('product')

    all_categories_found_list = []

    def find_all_ids():
        nonlocal all_categories_found
        categories_list = []
        for category in all_categories_found:
            categories_list.append(category.get('id'))

        return categories_list

    all_categories = find_all_ids()

    # with open(file_name, 'r', encoding='utf-8') as open_file:
    #     code = open_file.readlines()

    def find_categories(category_id):
        nonlocal offer_id, offer_line, errors_append, warnings_append
        nonlocal errors_list, all_categories_found, default_string, default_line

        count = 0
        for category in all_categories:
            if category == category_id:
                count += 1
                if count != 0:
                    all_categories_found_list.append(category_id)
                    break
        if count == 0 and category_id not in all_categories_found_list:
            errors_append(default_string + "Категория не представлена")

    default_line = 0

    def find_all_ids():
        nonlocal all_categories_found
        categories_list = []
        for category in all_categories_found:
            categories_list.append(category.get('id'))

        return categories_list

    def splitted_code():
        nonlocal default_line
        file_open = open(file_name, 'r', encoding='utf-8')
        splited_code = []
        found = False
        # Limit of lines - 500 per iteration
        for index, line in enumerate(file_open):
            if line.find('<offer') != -1:
                found = True
                splited_code.append(line)
            elif found:
                splited_code.append(line)
            default_line = index
            if (index + 1) % 500 == 0:
                parse_file(splited_code)
                del splited_code[:]

    def parse_file(splitted_code):
        pass


if __name__ == '__main__':
    compile_task()