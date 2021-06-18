from importing_modules import *


def compile_task():
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
                data.to_csv('databases/first_task_database.csv')

                page_index += 1
            else:
                print(f'Nothing has been found on {page_index} page.')
                break
        else:
            print(f'{page_index} page has not been found, status code of the page: {code.status_code}')
            break


if __name__ == '__main__':
    compile_task()
    print('First task completed!', end='\n')
    print('-=' * 20, end='\n')
