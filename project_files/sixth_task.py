from importing_modules import *


def compile_task():
    url_main = 'https://www.forward-sport.ru/bitrix/catalog_export/forward_stocks_250650.php'
    warnings_list = []

    code = requests.get(url_main)
    # with open(r'C:\Users\vladi\Downloads\forward_stocks_250650.xml', 'r', encoding='utf-8') as open_file:
    #     code = ''.join(open_file.readlines())
    soup_code = bs(code.text, 'lxml')

    offers_found = soup_code.find_all('offer')

    count_0 = 0
    count_1 = 0
    for index in range(len(offers_found)):
        if offers_found[index]['available'] == 'true':
            count_0 += 1
        if int(offers_found[index].find('quantity').text) > 0:
            count_1 += 1

    print(count_0)
    print(count_1)

    # for index in range(len(offers_found)):
    #     print(index, end=' ')
    #     found = offers_found[index].find_all('categoryid')
    #     if len(soup_code.find_all('category', {'id': found[0].text})) == 0:
    #         warnings_list.append(f'No category found [{offers_found[index]["id"]}: {found[0].text}]\n')
    #     if len(found) > 1:
    #         if len(soup_code.find_all('category', {'id': found[1].text})) == 0:
    #             warnings_list.append(f'No category found [{offers_found[index]["id"]}: {found[1].text}]\n')
    #     with open(f'forward_errors.txt', 'w', encoding='utf-8') as open_file_1:
    #         open_file_1.writelines(warnings_list)
    #
    # print()
    # print('Tags are done!')
    #
    # for index in range(len(offers_found)):
    #     if len(offers_found[index].find_all('picture')) < 1:  # Чтобы найти price, просто меняешь picture :D
    #         # print(offers_found[index].find('categoryid').text)
    #         # print('Error', index)
    #         # print(offers_found[index])
    #         warnings_list.append(f'No image found in offer id: {offers_found[index]["id"]}\n')
    #         with open(f'forward_errors.txt', 'w',
    #                   encoding='utf-8') as open_file_1:
    #             open_file_1.writelines(warnings_list)
    #
    # for index in range(len(offers_found)):
    #     if len(offers_found[index].find_all('price')) < 1:  # Чтобы найти price, просто меняешь picture :D
    #         # print(offers_found[index].find('categoryid').text)
    #         # print('Error', index)
    #         # print(offers_found[index])
    #         warnings_list.append(f'No price found in offer id: {offers_found[index]["id"]}\n')
    #         with open(f'forward_errors.txt', 'w',
    #                   encoding='utf-8') as open_file_1:
    #             open_file_1.writelines(warnings_list)
    #
    # os.startfile('forward_errors.txt')


if __name__ == '__main__':
    compile_task()
    print('First task completed!', end='\n')
    print('-=' * 20, end='\n')
