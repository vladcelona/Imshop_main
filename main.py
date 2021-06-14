from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


# First task
def parsing_function_replies():
    url_main = 'https://apps.shopify.com/plobalapps-mobile-application/reviews?page='
    columns = ['Name', 'Overall rating', 'Date of reply', 'Text']

    all_replies_dict = dict()
    all_replies_info = []

    page_index = 1
    while True:
        code = requests.get(url_main + str(page_index))
        if 200 >= code.status_code <= 299:
            soup_code = bs(code.text, 'lxml')

            all_replies_found = soup_code.find_all('div', {'class': 'review-listing'})
            if len(all_replies_found) > 0:
                for reply in all_replies_found:
                    all_replies_info.append(reply)

                for index in range(len(all_replies_info)):
                    all_replies_dict[index] = dict()
                    all_replies_dict[index][columns[0]] = all_replies_info[index].find('h3').text \
                        .strip().replace('\n', '')
                    all_replies_dict[index][columns[1]] = \
                        all_replies_info[index].find('span', {'class': 'ui-star-rating__rating visuallyhidden'}) \
                            .text.replace(' of ', '/')
                    all_replies_dict[index][columns[2]] = \
                        all_replies_info[index].find_all('div', {'class': 'review-metadata__item-value'})[1] \
                            .text.strip().replace('\n', '')
                    all_replies_dict[index][columns[3]] = all_replies_info[index].find('p').text.replace('\n', '')

                print(f'Parsing at page number {page_index} completed successfully!')

                data = pd.DataFrame(data=all_replies_dict, index=columns).T
                data.to_csv('replies_info.csv')

                page_index += 1
            else:
                print(f'Nothing has been found on {page_index} page.')
                return
        else:
            print(f'This page has not been found, status code of the page: {code.status_code}')
            return


# Second task
def parsing_function_app():
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
                data.to_csv('uk_companies_info.csv')

                print(f'Parsing at page number {page_index} completed successfully!')
                page_index += 1
        else:
            print(f'This page has not been found, status code of the page: {code.status_code}')
            break

    # data = pd.DataFrame(data=app_info_dict, index=columns).T
    # data.to_csv('uk_companies_info.csv')
    # data.to_csv('us_companies_info.csv')


if __name__ == '__main__':
    # parsing_function_replies()
    parsing_function_app()
