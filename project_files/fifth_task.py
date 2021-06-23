from importing_modules import *


def compile_task():
    files_list = ['forward_stocks_250650', 'yamlfeed1', 'yandex_01', 'yandex_utm', 'mobileapp']

    for file in files_list:
        new_warnings_filename = file + '_we1'
        warnings_list = []
        try:
            with open(rf'C:\Users\vladi\Downloads\{file}.xml', 'r', encoding='utf-8') as open_file:
                code = ''.join(open_file.readlines())
        except Exception:
            with open(rf'C:\Users\vladi\Downloads\{file}.xml', 'r') as open_file:
                code = ''.join(open_file.readlines())
        finally:
            print('This file is definitely broken...')

        soup_code = bs(code, 'lxml')
        offers_found = soup_code.find_all('offer')
        print(len(offers_found))

        for index in range(len(offers_found)):
            print(index, end=' ')
            found = offers_found[index].find_all('categoryid')
            if len(soup_code.find_all('category', {'id': found[0].text})) == 0:
                warnings_list.append(f'No category found [{offers_found[index]["id"]}: {found[0].text}]\n')
            if len(found) > 1:
                if len(soup_code.find_all('category', {'id': found[1].text})) == 0:
                    warnings_list.append(f'No category found [{offers_found[index]["id"]}: {found[1].text}]\n')
            with open(f'{new_warnings_filename}.txt', 'w', encoding='utf-8') as open_file_1:
                open_file_1.writelines(warnings_list)

        print()
        print('Tags are done!')

        for index in range(len(offers_found)):
            if len(offers_found[index].find_all('picture')) < 1:  # Чтобы найти price, просто меняешь picture :D
                # print(offers_found[index].find('categoryid').text)
                # print('Error', index)
                # print(offers_found[index])
                warnings_list.append(f'No image found in offer id: {offers_found[index]["id"]}\n')
                with open(f'{new_warnings_filename}.txt', 'w',
                          encoding='utf-8') as open_file_1:
                    open_file_1.writelines(warnings_list)

        for index in range(len(offers_found)):
            if len(offers_found[index].find_all('price')) < 1:  # Чтобы найти price, просто меняешь picture :D
                # print(offers_found[index].find('categoryid').text)
                # print('Error', index)
                # print(offers_found[index])
                warnings_list.append(f'No price found in offer id: {offers_found[index]["id"]}\n')
                with open(f'{new_warnings_filename}.txt', 'w',
                          encoding='utf-8') as open_file_1:
                    open_file_1.writelines(warnings_list)

        # with open(rf'C:\Users\vladi\Downloads\{new_warnings_filename}.txt', 'w', encoding='utf-8') as open_file_1:
        #     open_file_1.writelines(warnings_list)
        os.startfile(f'{new_warnings_filename}.txt')


if __name__ == '__main__':
    compile_task()
