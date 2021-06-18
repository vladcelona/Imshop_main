from importing_modules import *


def compile_task():
    url_main_1 = 'https://clutch.co/uk/app-developers?page='  # Change uk for us to search for the US companies
    url_main_2 = '&related_services=&related_services=field_pp_sl_ecommerce'  # Nothing should be changed here

    columns = ['Company name', 'Price']
    app_info_dict = dict()

    app_names_list = []
    app_prices_list = []

    page_index = 1
    while True:
        code = requests.get(url_main_1 + str(page_index) + url_main_2)
        if 200 >= code.status_code <= 299:
            soup_code = bs(code.text, 'lxml')

            app_names_local = soup_code.find_all('h3', {'class': 'company_info'})
            app_block_local = soup_code.find_all('div', {'class': 'list-item block_tag custom_popover'})

            for block in app_block_local:
                price_found = block.find('span').text
                app_prices_list.append(price_found)

            for name in app_names_local:
                app_names_list.append(name.text.strip().replace('\n', ''))

            if len(app_prices_list) != len(app_names_list):
                raise Exception('Lists have different length!')
            else:
                for index in range(len(app_prices_list)):
                    app_info_dict[index] = dict()
                    app_info_dict[index][columns[0]] = app_names_list[index]
                    app_info_dict[index][columns[1]] = app_prices_list[index]

                data = pd.DataFrame(data=app_info_dict, index=columns).T
                data.to_csv('databases/second_task_uk_database.csv')

                print(f'Parsing at page number {page_index} completed successfully!')
                page_index += 1
        else:
            print(f'{page_index} page has not been found, status code of the page: {code.status_code}')
            return


if __name__ == '__main__':
    compile_task()
    print('Second task completed!', end='\n')
    print('-=' * 20, end='\n')
