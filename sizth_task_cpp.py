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

        with open(local_filename, 'w') as open_file:
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

        with open(local_filename, 'w') as open_file:
            for chunk in tqdm.tqdm(code.iter_content(chunk_size=chunk_size), total=num_bars, unit='MB',
                                   desc=local_filename, leave=True, ncols=100, ascii=True):
                open_file.write(chunk)

        return

    else:
        file_size = len(code_1.text.split('\n'))
        num_bars = int(file_size / 2 ** 14)
        with open(local_filename, 'w') as open_file:
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

    cpp_file = open(r'C:\Users\vladi\CLionProjects\XML_Parser\main.cpp', 'r', encoding='utf-8')
    text = cpp_file.readlines()
    for index in range(len(text)):
        if ('R"(C:\\Users\\' in text[index]) and ('Xml::Inspector<Xml::Encoding::Utf8Writer>' in text[index]):
            text[index] = text[index][:text[index].index('R"(C:\\Users\\') + len(R"(C:")] + os.path.dirname(os.path.abspath(__file__)) \
                          + '\\' + file_name + ')");\n'

    cpp_file.close()

    print('File processing done!')

    with open(r'C:\Users\vladi\CLionProjects\XML_Parser\main.cpp', 'w', encoding='utf-8') as open_file:
        open_file.writelines(text)

    os.system('g++ C:\\Users\\vladi\\CLionProjects\\XML_Parser\\main.cpp -o C:\\Users\\vladi\\main.exe')
    print('Converting into .exe done!')
    os.system('C:\\Users\\vladi\\main.exe')

    def find_and_replace():
        all_categories = set()
        local_file_name = r'C:\Users\vladi\lines_columns_file.txt'
        rows_columns = [[int(line.split()[0]), int(line.split()[1])] for line in open(local_file_name, 'r', encoding='utf-8').readlines()[::2]]

        print(len(rows_columns))
        count = 0

        for row, column in rows_columns:
            if count % 100 == 0:
                print(count)
            cont = True
            for index, line in enumerate(open(file_name, 'r', encoding='utf-8')):
                if not cont:
                    break
                else:
                    # print(index)
                    if row - 1 == index:
                        word = ''
                        start_index = column - 1 + len('<categoryId>')
                        end_index = 0
                        for index_i in range(column - 1 + len('<categoryId>'), column - 1 + len('<categoryId>') + 2 ** 10):
                            if line[index_i] == '<':
                                cont = False
                                end_index = index_i
                                break
                            # print(line[index_i])
                            # word += line[index_i]
                        all_categories.add(line[start_index:end_index])

            count += 1

        for index, line in enumerate(open(local_file_name, 'r', encoding='utf-8')):
            pass

        print()
        all_categories = list(all_categories)

        for line in open(r'C:\Users\vladi\all_ids_found_file.txt', 'r', encoding='utf-8'):
            for category in all_categories:
                print(line.strip(), category.strip())
                if line == category:
                    pass

    find_and_replace()

    os.startfile(r'C:\Users\vladi\errors_cpp.txt')
    # os.startfile(r'C:\Users\vladi\additional_info_cpp.txt')
    os.startfile(r'C:\Users\vladi\lines_columns_file.txt')


if __name__ == '__main__':
    compile_task()